import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from apps.models.ingredient import Ingredient
from apps.daos.ingredient_dao import IngredientDAO  # Adjust the import path accordingly

@pytest.fixture
def ingredient_dao():
    return IngredientDAO()

@pytest.fixture
def mock_db_session():
    with patch('apps.db.session') as mock_session:
        yield mock_session

def test_get_ingredient_by_id(ingredient_dao, mock_db_session):
    ingredient_id = 1
    mock_ingredient = Ingredient(
        ingredientId=ingredient_id,
        ingredientName="Salt",
        category=1,
        nutrition={'calories': 0},
        createTime=datetime.utcnow(),
        modifyTime=datetime.utcnow()
    )
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_ingredient

    result = ingredient_dao.get_ingredient_by_id(ingredient_id)
    assert result['ingredientId'] == ingredient_id
    assert result['ingredientName'] == mock_ingredient.ingredientName
    assert result['category'] == mock_ingredient.category
    assert result['nutrition'] == mock_ingredient.nutrition

def test_get_ingredient_by_ids(ingredient_dao, mock_db_session):
    ingredient_ids = [1, 2, 3]
    ingredients = [
        Ingredient(
            ingredientId=1,
            ingredientName="Salt",
            category=1,
            nutrition={'calories': 0},
            createTime=datetime.utcnow(),
            modifyTime=datetime.utcnow()
        ),
        Ingredient(
            ingredientId=2,
            ingredientName="Sugar",
            category=2,
            nutrition={'calories': 400},
            createTime=datetime.utcnow(),
            modifyTime=datetime.utcnow()
        ),
        Ingredient(
            ingredientId=3,
            ingredientName="Pepper",
            category=1,
            nutrition={'calories': 10},
            createTime=datetime.utcnow(),
            modifyTime=datetime.utcnow()
        )
    ]
    mock_db_session.query.return_value.filter.return_value.all.return_value = ingredients

    result = ingredient_dao.get_ingredient_by_ids(ingredient_ids)
    assert len(result) == len(ingredients)
    for i, ingredient in enumerate(ingredients):
        assert result[i]['ingredientId'] == ingredient.ingredientId
        assert result[i]['ingredientName'] == ingredient.ingredientName
        assert result[i]['category'] == ingredient.category
        assert result[i]['nutrition'] == ingredient.nutrition

def test_get_ingredients_by_name(ingredient_dao, mock_db_session):
    ingredient_name = "Sugar"
    mock_ingredient = Ingredient(
        ingredientId=4,
        ingredientName=ingredient_name,
        category=2,
        nutrition={'calories': 400},
        createTime=datetime.utcnow(),
        modifyTime=datetime.utcnow()
    )
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_ingredient

    result = ingredient_dao.get_ingredients_by_name(ingredient_name)
    assert result['ingredientId'] == mock_ingredient.ingredientId
    assert result['ingredientName'] == mock_ingredient.ingredientName
    assert result['category'] == mock_ingredient.category
    assert result['nutrition'] == mock_ingredient.nutrition

def test_add_ingredient(ingredient_dao, mock_db_session):
    ingredient_name = "Salt"
    category = 1

    # Mock the add method to mimic adding an object to the session
    def mock_add(instance):
        instance.ingredientId = 10  # Set a mock primary key
        return instance

    # Assign mock implementation to the session methods
    mock_db_session.add.side_effect = mock_add
    mock_db_session.flush = MagicMock()

    # Call the DAO method
    new_ingredient_id = ingredient_dao.add_ingredient(ingredient_name, category)

    # Assertions to verify interactions and correctness
    mock_db_session.add.assert_called_once()  # Ensure add was called
    mock_db_session.flush.assert_called_once()  # Ensure flush was called
    assert new_ingredient_id == 10  # Check that the primary key is as expected

