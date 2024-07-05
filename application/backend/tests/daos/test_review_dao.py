import pytest
from unittest.mock import patch, MagicMock
from apps.daos.review_dao import ReviewDAO
from apps.models.review import Review

@pytest.fixture
def review_dao():
    return ReviewDAO()

@pytest.fixture
def mock_db_session():
    with patch('apps.db.session') as mock_session:
        yield mock_session

def test_get_review_by_recipe(review_dao, mock_db_session):
    recipe_id = 1
    mock_reviews = [
        Review(reviewId=1, userId=1, recipeId=recipe_id, comment="Good", rating=4, status=1),
        Review(reviewId=2, userId=2, recipeId=recipe_id, comment="Excellent", rating=5, status=1)
    ]
    for mock_review in mock_reviews:
        mock_review.to_dict = MagicMock(return_value={
            'reviewId': mock_review.reviewId,
            'userId': mock_review.userId,
            'recipeId': mock_review.recipeId,
            'comment': mock_review.comment,
            'rating': mock_review.rating,
            'status': mock_review.status
        })

    mock_db_session.query.return_value.filter.return_value.all.return_value = mock_reviews

    result = review_dao.get_review_by_recipe(recipe_id)
    assert len(result) == len(mock_reviews)
    for i, review in enumerate(result):
        review_dict = review.to_dict()  # Call the mocked to_dict method
        assert review_dict['reviewId'] == mock_reviews[i].reviewId
        assert review_dict['userId'] == mock_reviews[i].userId
        assert review_dict['recipeId'] == mock_reviews[i].recipeId
        assert review_dict['comment'] == mock_reviews[i].comment
        assert review_dict['rating'] == mock_reviews[i].rating
        assert review_dict['status'] == mock_reviews[i].status

def test_add_review(review_dao, mock_db_session):
    user_id = 1
    recipe_id = 2
    comment = "Nice"
    rating = 5

    mock_review = MagicMock()
    mock_review.reviewId = 3
    mock_db_session.add.side_effect = lambda x: setattr(x, 'reviewId', 3)
    mock_db_session.commit = MagicMock()

    review_dao.add_review(user_id, recipe_id, comment, rating)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
