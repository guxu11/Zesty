import pytest
from unittest.mock import patch, MagicMock
from apps.services.user_ingredient_service import UserIngredientService, UserIngredientResponseStatus
from apps.daos.userIngredient_dao import UserIngredientDAO
from apps.daos.ingredient_dao import IngredientDAO
from apps.daos.recipeIngredient_dao import RecipeIngredientDAO

@pytest.fixture
def user_ingredient_service():
    with patch('apps.services.user_ingredient_service.UserIngredientDAO') as mock_user_ingredient_dao, \
         patch('apps.services.user_ingredient_service.IngredientDAO') as mock_ingredient_dao, \
         patch('apps.services.user_ingredient_service.RecipeIngredientDAO') as mock_recipe_ingredient_dao:
        
        service = UserIngredientService()
        service.userIngredeint_dao = mock_user_ingredient_dao.return_value
        service.ingredient_dao = mock_ingredient_dao.return_value
        service.recipeIngredient_dao = mock_recipe_ingredient_dao.return_value

        yield service



def test_get_user_ingredients_with_ingredients(user_ingredient_service):
    user_ingredients = [{"ingredientId": 1}, {"ingredientId": 2}]
    user_ingredient_service.userIngredeint_dao.get_user_ingredients_by_userId.return_value = user_ingredients
    user_ingredient_service.ingredient_dao.get_ingredient_by_id.side_effect = [
        {"ingredientName": "Tomato"}, {"ingredientName": "Basil"}
    ]

    response = user_ingredient_service.get_userIngredients(1)

    assert "data" in response
    assert response["data"] == ["Tomato", "Basil"]
    # Updated expected status code to match what is returned by SUCCESS status
    assert response["statusCode"] == UserIngredientResponseStatus.SUCCESS["statusCode"]



def test_get_missing_ingredients(user_ingredient_service):
    recipe_ingredients = [{"ingredientId": 1}, {"ingredientId": 2}, {"ingredientId": 3}]
    user_ingredients = [{"ingredientId": 1}, {"ingredientId": 3}]
    missing_ingredient_ids = [{"ingredientId": 2, "ingredientName": "Basil"}]
    user_ingredient_service.recipeIngredient_dao.get_ingredients_by_recipeId.return_value = recipe_ingredients
    user_ingredient_service.userIngredeint_dao.get_user_ingredients_by_userId.return_value = user_ingredients
    user_ingredient_service.ingredient_dao.get_ingredient_by_ids.return_value = missing_ingredient_ids

    response = user_ingredient_service.get_missingIngredients(1, 1)

    assert "data" in response
    assert response["data"]["missing_ingredients"] == missing_ingredient_ids
    # Compare rounded values to avoid precision issues
    assert round(response["data"]["percent_incommon"], 2) == round(66.67, 2)
    assert response["statusCode"] == UserIngredientResponseStatus.SUCCESS["statusCode"]

