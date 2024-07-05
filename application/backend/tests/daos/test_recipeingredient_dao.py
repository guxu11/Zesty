import pytest
from unittest.mock import patch, MagicMock
from apps.daos.recipeIngredient_dao import RecipeIngredientDAO
from apps.models.recipeIngredient import RecipeIngredient

@pytest.fixture
def recipe_ingredient_dao():
    return RecipeIngredientDAO()

@pytest.fixture
def mock_db_session():
    with patch('apps.db.session') as mock_session:
        yield mock_session

def test_get_recipeIngredient_by_id(recipe_ingredient_dao, mock_db_session):
    recipe_ingredient_id = 1
    mock_ingredient = MagicMock(spec=RecipeIngredient)
    mock_ingredient.recipeIngredientId = recipe_ingredient_id
    mock_ingredient.ingredientId = 2
    mock_ingredient.recipeId = 3
    mock_ingredient.amount = "100g"
    mock_ingredient.to_dict.return_value = {
        'recipeIngredientId': recipe_ingredient_id,
        'ingredientId': 2,
        'recipeId': 3,
        'amount': "100g"
    }

    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_ingredient

    result = recipe_ingredient_dao.get_recipeIngredient_by_id(recipe_ingredient_id)

    assert result['recipeIngredientId'] == recipe_ingredient_id
    assert result['ingredientId'] == 2
    assert result['recipeId'] == 3
    assert result['amount'] == "100g"

def test_get_ingredients_by_recipeId(recipe_ingredient_dao, mock_db_session):
    recipe_id = 3
    mock_ingredients = []
    for recipe_ingredient_id, ingredient_id, amount in [(1, 2, "50g"), (2, 3, "30g")]:
        mock_ingredient = MagicMock(spec=RecipeIngredient)
        mock_ingredient.recipeIngredientId = recipe_ingredient_id
        mock_ingredient.ingredientId = ingredient_id
        mock_ingredient.recipeId = recipe_id
        mock_ingredient.amount = amount
        mock_ingredient.to_dict.return_value = {
            'recipeIngredientId': recipe_ingredient_id,
            'ingredientId': ingredient_id,
            'recipeId': recipe_id,
            'amount': amount
        }
        mock_ingredients.append(mock_ingredient)

    mock_db_session.query.return_value.filter.return_value.all.return_value = mock_ingredients

    result = recipe_ingredient_dao.get_ingredients_by_recipeId(recipe_id)

    assert len(result) == 2
    assert result[0]['recipeIngredientId'] == 1
    assert result[0]['ingredientId'] == 2
    assert result[0]['recipeId'] == recipe_id
    assert result[0]['amount'] == "50g"
    assert result[1]['recipeIngredientId'] == 2
    assert result[1]['ingredientId'] == 3
    assert result[1]['recipeId'] == recipe_id
    assert result[1]['amount'] == "30g"

def test_add_recipeIngredient(recipe_ingredient_dao, mock_db_session):
    recipe_id = 3
    ingredient_id = 2
    amount = "200g"

    mock_ingredient = MagicMock()
    mock_ingredient.recipeIngredientId = 5
    mock_db_session.add.side_effect = lambda x: setattr(x, 'recipeIngredientId', 5)

    new_recipe_ingredient_id = recipe_ingredient_dao.add_recipeIngredient(recipe_id, ingredient_id, amount)

    assert new_recipe_ingredient_id == 5
    mock_db_session.add.assert_called_once()
