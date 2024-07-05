import pytest
from unittest.mock import patch, MagicMock
from apps.common.transaction_processor import transactional
from sqlalchemy.exc import SQLAlchemyError

@pytest.fixture
def mock_session():
    with patch('apps.db.session') as mock_session:
        yield mock_session

def test_transactional_success(mock_session):
    @transactional()
    def example_function():
        return "success"

    result = example_function()
    mock_session.begin.assert_called_once()
    mock_session.commit.assert_called_once()
    assert result == "success"

def test_transactional_failure(mock_session):
    @transactional()
    def example_function():
        raise SQLAlchemyError("Test Error")

    with pytest.raises(SQLAlchemyError):
        example_function()
    mock_session.begin.assert_called_once()
    mock_session.rollback.assert_called_once()

