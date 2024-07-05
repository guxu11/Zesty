import pytest
from unittest.mock import patch, MagicMock
from apps.models.favorite import Favorite
from apps.daos.favorite_dao import FavoriteDAO  # Adjust this import based on the actual location

@pytest.fixture
def favorite_dao():
    return FavoriteDAO()

@pytest.fixture
def mock_db_session():
    with patch('apps.db.session') as mock_session:
        yield mock_session

def test_get_favorite_by_user(favorite_dao, mock_db_session):
    user_id = 1
    mock_favorite = MagicMock(spec=Favorite)
    mock_favorite.userId = user_id
    mock_db_session.query.return_value.filter.return_value.all.return_value = [mock_favorite]

    result = favorite_dao.get_favorite_by_user(user_id)

    assert len(result) == 1
    assert result[0].userId == user_id

def test_get_favorite_by_user_and_recipe(favorite_dao, mock_db_session):
    user_id = 1
    recipe_id = 1
    mock_favorite = MagicMock(spec=Favorite)
    mock_favorite.userId = user_id
    mock_favorite.recipeId = recipe_id
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_favorite

    result = favorite_dao.get_favorite_by_user_and_recipe(user_id, recipe_id)

    assert result is not None
    assert result.userId == user_id
    assert result.recipeId == recipe_id

def test_add_favorite(favorite_dao, mock_db_session):
    user_id = 1
    recipe_id = 1
    favorite_dao.add_favorite(user_id, recipe_id)

    assert mock_db_session.add.called
    assert mock_db_session.commit.called

def test_change_favorite(favorite_dao, mock_db_session):
    mock_favorite = MagicMock(spec=Favorite)
    mock_favorite.status = 1
    favorite_dao.change_favorite(mock_favorite, 0)

    assert mock_favorite.status == 0
    assert mock_db_session.commit.called
