import pytest
from unittest.mock import patch, MagicMock
from apps.daos.userIngredient_dao import UserIngredientDAO
from apps.models.userIngredient import UserIngredient

@pytest.fixture
def user_ingredient_dao():
    return UserIngredientDAO()

@pytest.fixture
def mock_db_session():
    with patch('apps.db.session') as mock_session:
        yield mock_session

def test_add_user_ingredient(user_ingredient_dao, mock_db_session):
    ingredient_id = 1
    user_id = 2
    mock_user_ingredient = MagicMock()
    mock_user_ingredient.ingredientId = ingredient_id

    mock_db_session.add.side_effect = lambda x: setattr(x, 'userIngredientId', 10)
    mock_db_session.flush = MagicMock()

    result = user_ingredient_dao.add_user_ingredient(ingredient_id, user_id)

    assert result == ingredient_id
    mock_db_session.add.assert_called_once()
    mock_db_session.flush.assert_called_once()

def test_delete_user_ingredient_by_id(user_ingredient_dao, mock_db_session):
    ingredient_id = 1
    user_id = 2
    mock_user_ingredient = MagicMock()
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user_ingredient

    user_ingredient_dao.delete_user_ingredient_by_id(ingredient_id, user_id)

    mock_db_session.delete.assert_called_once_with(mock_user_ingredient)
    mock_db_session.commit.assert_called_once()

def test_get_user_ingredients_by_userId(user_ingredient_dao, mock_db_session):
    user_id = 2
    mock_user_ingredient_1 = MagicMock()
    mock_user_ingredient_2 = MagicMock()
    mock_user_ingredient_1.to_dict = MagicMock(return_value={'userIngredientId': 10, 'ingredientId': 1, 'userId': user_id})
    mock_user_ingredient_2.to_dict = MagicMock(return_value={'userIngredientId': 11, 'ingredientId': 2, 'userId': user_id})

    mock_db_session.query.return_value.filter.return_value.all.return_value = [mock_user_ingredient_1, mock_user_ingredient_2]

    result = user_ingredient_dao.get_user_ingredients_by_userId(user_id)

    assert result == [mock_user_ingredient_1.to_dict(), mock_user_ingredient_2.to_dict()]
    mock_db_session.query.return_value.filter.return_value.all.assert_called_once()

def test_get_user_ingredient_by_ingredientId(user_ingredient_dao, mock_db_session):
    ingredient_id = 1
    user_id = 2
    mock_user_ingredient = MagicMock()
    mock_user_ingredient.to_dict = MagicMock(return_value={'userIngredientId': 10, 'ingredientId': ingredient_id, 'userId': user_id})

    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user_ingredient

    result = user_ingredient_dao.get_user_ingredient_by_ingredientId(ingredient_id, user_id)

    assert result == mock_user_ingredient
    mock_db_session.query.return_value.filter.return_value.first.assert_called_once()
