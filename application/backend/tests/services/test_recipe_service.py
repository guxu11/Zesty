import pytest
from unittest.mock import patch, MagicMock
from apps.services.recipe_service import RecipeService, RecipeDetailResponseStatus, SearchResponseStatus, CreateRecipeResponseStatus, PantryRecipesResponseStatus

@pytest.fixture
def recipe_service():
    with patch('apps.services.recipe_service.RecipeDAO') as mock_recipe_dao, \
         patch('apps.services.recipe_service.IngredientDAO') as mock_ingredient_dao, \
         patch('apps.services.recipe_service.RecipeIngredientDAO') as mock_recipe_ingredient_dao, \
         patch('apps.services.recipe_service.ReviewDAO') as mock_review_dao, \
         patch('apps.services.recipe_service.UserDAO') as mock_user_dao, \
         patch('apps.services.recipe_service.UserIngredientDAO') as mock_user_ingredient_dao:
        
        service = RecipeService()
        service.recipe_dao = mock_recipe_dao.return_value
        service.ingredient_dao = mock_ingredient_dao.return_value
        service.recipe_ingredient_dao = mock_recipe_ingredient_dao.return_value
        service.review_dao = mock_review_dao.return_value
        service.user_dao = mock_user_dao.return_value
        service.user_ingredient_dao = mock_user_ingredient_dao.return_value

        yield service

def test_get_recipe_detail_by_id_found(recipe_service):
    mock_recipe = {"recipeId": 1, "recipeName": "Pasta"}
    recipe_service.recipe_dao.get_recipe_by_id.return_value = mock_recipe
    recipe_service.review_dao.get_avg_score_by_recipeId.return_value = 4.5
    recipe_service.recipe_ingredient_dao.get_ingredients_by_recipeId.return_value = [
        {"ingredientId": 1, "amount": "100g"}
    ]
    recipe_service.ingredient_dao.get_ingredient_by_id.return_value = {
        "ingredientId": 1, "ingredientName": "Tomato"
    }
    recipe_service.review_dao.get_review_by_recipe.return_value = [
        MagicMock(to_dict=lambda: {"userId": 1, "comment": "Good!"})
    ]
    recipe_service.user_dao.get_user_by_id.return_value = MagicMock(to_dict=lambda: {"userName": "Alice"})

    response = recipe_service.get_recipe_detail_by_id(1)

    assert response["data"]["recipeId"] == 1
    assert response["data"]["rating"] == 4.5
    assert response["data"]["reviews"][0]["userName"] == "Alice"

def test_get_recipe_detail_by_id_not_found(recipe_service):
    recipe_service.recipe_dao.get_recipe_by_id.return_value = None

    response = recipe_service.get_recipe_detail_by_id(999)

    assert response == {
        "statusCode": RecipeDetailResponseStatus.RECIPE_NOT_FOUND["statusCode"],
        "statusMessage": RecipeDetailResponseStatus.RECIPE_NOT_FOUND["statusMessage"].format(999)
    }



def test_get_random_recipes(recipe_service):
    random_recipes = [{"recipeId": 1, "recipeName": "Pasta"}]
    recipe_service.recipe_dao.get_random_recipes.return_value = random_recipes
    recipe_service.review_dao.get_avg_score_by_recipeIds.return_value = {1: 4.5}

    response = recipe_service.get_random_recipes()

    assert response["data"][0]["recipeName"] == "Pasta"
    assert response["data"][0]["rating"] == 4.5

def test_get_recipes_by_pantry_no_ingredients(recipe_service):
    recipe_service.user_ingredient_dao.get_user_ingredients_by_userId.return_value = None

    response = recipe_service.get_recipes_by_pantry(1)

    assert response == PantryRecipesResponseStatus.NO_INGREDIENTS

def test_get_recipes_by_pantry_no_matched_recipes(recipe_service):
    recipe_service.user_ingredient_dao.get_user_ingredients_by_userId.return_value = [{"ingredientId": 1}]
    recipe_service.recipe_ingredient_dao.get_ingredients_by_ingredientId.return_value = None

    response = recipe_service.get_recipes_by_pantry(1)

    assert response == PantryRecipesResponseStatus.NO_RECIPES_MATCHED_PANTRY

def test_get_recipes_by_pantry_with_matched_recipes(recipe_service):
    user_ingredients = [{"ingredientId": 1}]
    recipe_service.user_ingredient_dao.get_user_ingredients_by_userId.return_value = user_ingredients
    recipe_service.recipe_ingredient_dao.get_ingredients_by_ingredientId.return_value = [
        {"recipeId": 1}
    ]
    recipe_service.recipe_dao.get_recipes_preview_by_id.return_value = {"recipeId": 1, "recipeName": "Pasta"}
    recipe_service.recipe_ingredient_dao.get_ingredients_by_recipeId.return_value = [
        {"ingredientId": 1}
    ]
    recipe_service.review_dao.get_avg_score_by_recipeIds.return_value = {1: 4.5}

    def calculate_completeness(user_ingredient_ids, recipe_ingredient_ids):
        return 100 if user_ingredient_ids == recipe_ingredient_ids else 0

    with patch('apps.services.recipe_service.calculate_completeness', calculate_completeness):
        response = recipe_service.get_recipes_by_pantry(1)

    assert "data" in response
    assert response["data"][0]["recipeName"] == "Pasta"
    assert response["data"][0]["rating"] == 4.5
    assert response["data"][0]["completeness"] == 100

