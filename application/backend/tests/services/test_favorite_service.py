import pytest
from unittest.mock import MagicMock, patch
from apps.services.favorite_service import FavoriteService, FavoriteResponse

@pytest.fixture
def favorite_service():
    with patch('apps.services.favorite_service.FavoriteDAO') as mock_favorite_dao, \
         patch('apps.services.favorite_service.RecipeDAO') as mock_recipe_dao, \
         patch('apps.services.favorite_service.ReviewDAO') as mock_review_dao:
        
        mock_favorite_dao_instance = mock_favorite_dao.return_value
        mock_recipe_dao_instance = mock_recipe_dao.return_value
        mock_review_dao_instance = mock_review_dao.return_value

        service = FavoriteService()
        service.favorite_dao = mock_favorite_dao_instance
        service.recipe_dao = mock_recipe_dao_instance
        service.review_dao = mock_review_dao_instance

        yield service

def test_add_favorite_existing(favorite_service):
    favorite_service.favorite_dao.get_favorite_by_user_and_recipe.return_value = MagicMock(status=1)

    input_data = {"userId": 1, "recipeId": 1}
    response = favorite_service.add_favorite(input_data)

    favorite_service.favorite_dao.change_favorite.assert_called_once()
    assert response == FavoriteResponse.SUCCESS

def test_add_favorite_new(favorite_service):
    favorite_service.favorite_dao.get_favorite_by_user_and_recipe.return_value = None

    input_data = {"userId": 1, "recipeId": 1}
    response = favorite_service.add_favorite(input_data)

    favorite_service.favorite_dao.add_favorite.assert_called_once()
    assert response == FavoriteResponse.SUCCESS

def test_get_favorite_status(favorite_service):
    favorite = MagicMock()
    favorite.to_dict.return_value = {"status": 1}
    favorite_service.favorite_dao.get_favorite_by_user_and_recipe.return_value = favorite

    input_data = {"userId": 1, "recipeId": 1}
    response = favorite_service.get_favorite_status(input_data)

    assert response["data"]["status"] == 1

def test_get_user_favorites(favorite_service):
    favorite_service.favorite_dao.get_favorite_by_user.return_value = [MagicMock(recipeId=1)]
    favorite_service.recipe_dao.get_recipes_preview_by_id.return_value = {
        "recipeName": "Pasta",
        "recipeId": 1,
    }
    favorite_service.review_dao.get_avg_score_by_recipeId.return_value = 4.5

    input_data = 1
    response = favorite_service.get_user_favorites(input_data)

    assert response["data"][0]["recipeName"] == "Pasta"
    assert response["data"][0]["rating"] == 4.5
