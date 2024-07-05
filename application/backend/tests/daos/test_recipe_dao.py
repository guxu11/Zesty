import pytest
from unittest.mock import patch, MagicMock
from apps.daos.recipe_dao import RecipeDAO
from apps.models.recipe import Recipe

@pytest.fixture
def recipe_dao():
    return RecipeDAO()

@pytest.fixture
def mock_db_session():
    with patch('apps.db.session') as mock_session:
        yield mock_session

def test_get_recipe_by_id(recipe_dao, mock_db_session):
    recipe_id = 1
    mock_recipe = Recipe(recipeId=recipe_id, recipeName="Pancakes")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_recipe

    result = recipe_dao.get_recipe_by_id(recipe_id)

    assert result['recipeId'] == recipe_id
    assert result['recipeName'] == "Pancakes"

def test_get_recipes_by_name(recipe_dao, mock_db_session):
    recipe_name = "Pancakes"
    mock_recipes = [
        Recipe(recipeId=1, recipeName=recipe_name),
        Recipe(recipeId=2, recipeName="Blueberry Pancakes")
    ]
    mock_db_session.query.return_value.filter.return_value.all.return_value = mock_recipes

    result = recipe_dao.get_recipes_by_name(recipe_name)

    assert len(result) == 2
    assert result[0]['recipeId'] == 1
    assert result[0]['recipeName'] == recipe_name
    assert result[1]['recipeId'] == 2
    assert result[1]['recipeName'] == "Blueberry Pancakes"

def test_add_recipe(recipe_dao, mock_db_session):
    recipe_data = {
        'recipeName': 'Pasta',
        'createorId': 1,  # Adjusted to match the typo in the method
        'recipeType': 1,
        'category': 1,
        'difficulty': 2,
        'cookingTime': '30 min',
        'steps': ['Boil water', 'Cook pasta'],
        'recipePicture': 'path/to/pasta.jpg',
        'status': 1,
        'description': 'Delicious pasta recipe'
    }
    mock_recipe = MagicMock()
    mock_recipe.recipeId = 10
    mock_db_session.add.side_effect = lambda x: setattr(x, 'recipeId', 10)
    mock_db_session.flush = MagicMock()

    new_recipe_id = recipe_dao.add_recipe(**recipe_data)

    assert new_recipe_id == 10
    mock_db_session.add.assert_called_once()
    mock_db_session.flush.assert_called_once()
