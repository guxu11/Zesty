import pytest
from apps.common.search_engine import SearchEngine

@pytest.fixture
def search_engine():
    return SearchEngine()

def test_extract_text(search_engine):
    text = "Beef, chicken, and pork are all types of meat."
    expected_output = "beef chicken and pork are all type of meat"
    assert search_engine.extract_text(text) == expected_output

def test_fuzzy_match(search_engine):
    query = "chiken"
    choices = ["beef", "chicken", "pork"]
    expected_output = "chicken"
    assert search_engine.fuzzy_match(query, choices) == expected_output
