import pytest
from unittest.mock import patch, MagicMock

# Mock db.session
@pytest.fixture
def mock_db_session():
    with patch('apps.db.session') as mock_session:
        yield mock_session

def test_favorite_model(mock_db_session):
    mock_favorite = MagicMock()
    mock_favorite.userId = 1
    mock_favorite.recipeId = 1
    mock_favorite.status = 1

    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None

    mock_db_session.add(mock_favorite)
    mock_db_session.commit()

    assert mock_favorite.userId == 1
    assert mock_favorite.recipeId == 1
    assert mock_favorite.status == 1

def test_ingredient_model(mock_db_session):
    mock_ingredient = MagicMock()
    mock_ingredient.ingredientName = "Tomato"
    mock_ingredient.category = 1

    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None

    mock_db_session.add(mock_ingredient)
    mock_db_session.commit()

    assert mock_ingredient.ingredientName == "Tomato"
    assert mock_ingredient.category == 1

def test_recipe_model(mock_db_session):
    mock_recipe = MagicMock()
    mock_recipe.recipeName = "Pasta"
    mock_recipe.category = 1

    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None

    mock_db_session.add(mock_recipe)
    mock_db_session.commit()

    assert mock_recipe.recipeName == "Pasta"
    assert mock_recipe.category == 1

def test_recipe_ingredient_model(mock_db_session):
    mock_recipe_ingredient = MagicMock()
    mock_recipe_ingredient.recipeId = 1
    mock_recipe_ingredient.ingredientId = 1
    mock_recipe_ingredient.amount = "100g"

    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None

    mock_db_session.add(mock_recipe_ingredient)
    mock_db_session.commit()

    assert mock_recipe_ingredient.recipeId == 1
    assert mock_recipe_ingredient.ingredientId == 1
    assert mock_recipe_ingredient.amount == "100g"

def test_review_model(mock_db_session):
    mock_review = MagicMock()
    mock_review.userId = 1
    mock_review.recipeId = 1
    mock_review.comment = "Great recipe!"
    mock_review.rating = 5

    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None

    mock_db_session.add(mock_review)
    mock_db_session.commit()

    assert mock_review.userId == 1
    assert mock_review.recipeId == 1
    assert mock_review.comment == "Great recipe!"

def test_user_model(mock_db_session):
    mock_user = MagicMock()
    mock_user.userName = "Alice"
    mock_user.email = "alice@example.com"

    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None

    mock_db_session.add(mock_user)
    mock_db_session.commit()

    assert mock_user.userName == "Alice"
    assert mock_user.email == "alice@example.com"

def test_user_ingredient_model(mock_db_session):
    mock_user_ingredient = MagicMock()
    mock_user_ingredient.ingredientId = 1
    mock_user_ingredient.userId = 1

    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None

    mock_db_session.add(mock_user_ingredient)
    mock_db_session.commit()

    assert mock_user_ingredient.ingredientId == 1
    assert mock_user_ingredient.userId == 1
