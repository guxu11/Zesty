import pytest
from unittest.mock import patch, MagicMock
from apps.daos.user_dao import UserDAO
from apps.models.user import User

@pytest.fixture
def user_dao():
    return UserDAO()

@pytest.fixture
def mock_db_session():
    with patch('apps.db.session') as mock_session:
        yield mock_session

def test_get_user_by_id(user_dao, mock_db_session):
    user_id = 1
    mock_user = User(userId=user_id, userName="testuser", email="test@example.com")
    mock_user.to_dict = MagicMock(return_value={
        'userId': user_id,
        'userName': mock_user.userName,
        'email': mock_user.email,
        'userType': mock_user.userType
    })

    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user

    result = user_dao.get_user_by_id(user_id)
    assert result.userId == user_id

def test_get_user_by_email(user_dao, mock_db_session):
    email = "test@example.com"
    mock_user = User(userId=1, userName="testuser", email=email)
    mock_user.to_dict = MagicMock(return_value={
        'userId': mock_user.userId,
        'userName': mock_user.userName,
        'email': email,
        'userType': mock_user.userType
    })

    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user

    result = user_dao.get_user_by_email(email)
    assert result.email == email

def test_add_user(user_dao, mock_db_session):
    user_name = "testuser"
    email = "test@example.com"
    password = "testpassword"
    user_type = 3

    mock_user = MagicMock()
    mock_user.userId = 1
    mock_db_session.add.side_effect = lambda x: setattr(x, 'userId', 1)
    mock_db_session.commit = MagicMock()

    user_dao.add_user(userName=user_name, email=email, password=password, userType=user_type)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
