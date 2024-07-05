import pytest
from unittest.mock import patch, MagicMock
from apps.services.review_service import ReviewService, ReviewResponse

@pytest.fixture
def review_service():
    with patch('apps.services.review_service.ReviewDAO') as mock_review_dao:
        mock_review_dao_instance = mock_review_dao.return_value
        service = ReviewService()
        service.review_dao = mock_review_dao_instance
        yield service

def test_add_review_existing(review_service):
    review_service.review_dao.get_review_by_user_and_recipe.return_value = MagicMock()

    response = review_service.add_review(1, 1, "Great recipe!", 5)

    review_service.review_dao.update_review.assert_called_once_with(1, 1, "Great recipe!", 5)
    assert response == ReviewResponse.SUCCESS

def test_add_review_new(review_service):
    review_service.review_dao.get_review_by_user_and_recipe.return_value = None

    response = review_service.add_review(1, 1, "Loved it!", 4)

    review_service.review_dao.add_review.assert_called_once_with(1, 1, "Loved it!", 4)
    assert response == ReviewResponse.SUCCESS

def test_add_review_no_comment_or_rating(review_service):
    response = review_service.add_review(1, 1, None, None)

    assert response == ReviewResponse.No_Comment_Or_Rate

def test_get_avg(review_service):
    review_service.review_dao.get_avg_rating.return_value = 4.0

    response = review_service.get_avg(1)

    assert response['data'] == 4.0
    assert response['statusCode'] == ReviewResponse.SUCCESS['statusCode']
    assert response['statusMessage'] == ReviewResponse.SUCCESS['statusMessage']
