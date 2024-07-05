import pytest
from unittest.mock import MagicMock, patch
from apps.services.user_profile_service import UserProfileService, RegisterResponse, LoginResponse
from apps.enums.response_status import ResponseStatus

@pytest.fixture
def user_profile_service():
    with patch('apps.services.user_profile_service.UserDAO') as mock_user_dao, \
         patch('apps.services.user_profile_service.RecipeDAO') as mock_recipe_dao, \
         patch('apps.services.user_profile_service.ReviewDAO') as mock_review_dao:

        service = UserProfileService()
        service.user_dao = mock_user_dao.return_value
        service.recipe_dao = mock_recipe_dao.return_value
        service.review_dao = mock_review_dao.return_value

        yield service

def test_register_success(user_profile_service):
    user_profile_service.user_dao.get_user_by_email.return_value = None
    user_profile_service.user_dao.add_user.return_value = {"userId": 1, "name": "John Doe", "email": "john.doe@example.com"}

    response = user_profile_service.register("John Doe", "john.doe@example.com", "password123")

    assert response["statusCode"] == RegisterResponse.SUCCESS["statusCode"]
    user_profile_service.user_dao.get_user_by_email.assert_called_with("john.doe@example.com")
    user_profile_service.user_dao.add_user.assert_called()

def test_register_email_exists(user_profile_service):
    user_profile_service.user_dao.get_user_by_email.return_value = {"userId": 1, "name": "Existing User"}

    response = user_profile_service.register("Jane Doe", "existing@example.com", "password123")

    assert response["statusCode"] == RegisterResponse.EMAIL_EXIST["statusCode"]
    user_profile_service.user_dao.get_user_by_email.assert_called_with("existing@example.com")
    user_profile_service.user_dao.add_user.assert_not_called()

def test_login_success(user_profile_service):
    user_mock = MagicMock()
    user_mock.verify_password.return_value = True
    user_mock.to_dict.return_value = {"userId": 1, "name": "John Doe", "email": "john.doe@example.com"}
    user_profile_service.user_dao.get_user_by_email.return_value = user_mock

    response = user_profile_service.login("john.doe@example.com", "password123")

    assert response["statusCode"] == LoginResponse.SUCCESS["statusCode"]
    assert "data" in response
    user_mock.verify_password.assert_called_with("password123")

def test_login_user_not_exist(user_profile_service):
    user_profile_service.user_dao.get_user_by_email.return_value = None

    response = user_profile_service.login("unknown@example.com", "password123")

    assert response["statusCode"] == LoginResponse.USER_NOT_EXIST["statusCode"]
    user_profile_service.user_dao.get_user_by_email.assert_called_with("unknown@example.com")

def test_login_wrong_password(user_profile_service):
    user_mock = MagicMock()
    user_mock.verify_password.return_value = False
    user_profile_service.user_dao.get_user_by_email.return_value = user_mock

    response = user_profile_service.login("john.doe@example.com", "wrongpassword")

    assert response["statusCode"] == LoginResponse.WRONG_PASSWORD["statusCode"]
    user_mock.verify_password.assert_called_with("wrongpassword")

def test_get_posted_recipes(user_profile_service):
    user_id = 1
    recipes = [{"recipeId": 1, "title": "Pasta"}, {"recipeId": 2, "title": "Salad"}]
    recipe_ratings = {1: 4.5, 2: 3.8}
    user_profile_service.recipe_dao.get_recipes_preview_by_creator.return_value = recipes
    user_profile_service.review_dao.get_avg_score_by_recipeId.side_effect = lambda recipe_id: recipe_ratings[recipe_id]

    response = user_profile_service.get_posted_recipes(user_id)

    assert response["statusCode"] == ResponseStatus.SUCCESS["statusCode"]
    assert "data" in response
    assert len(response["data"]) == 2
    for recipe in response["data"]:
        assert "rating" in recipe

def test_get_posted_recipes_invalid_input(user_profile_service):
    response = user_profile_service.get_posted_recipes(None)

    assert response["statusCode"] == ResponseStatus.FAIL["statusCode"]
