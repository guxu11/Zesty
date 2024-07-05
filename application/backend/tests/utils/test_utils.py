import pytest
from apps.utils.utils import gen_random_string, calculate_completeness  # Replace with your actual module

def test_gen_random_string():
    # Test the length of the generated string
    random_string = gen_random_string(50)
    assert len(random_string) == 60  # 50 + 10 (approximate length of timestamp)

    # Test for randomization by generating multiple strings
    strings = {gen_random_string(50) for _ in range(100)}
    assert len(strings) == 100  # Expect all 100 to be unique

def test_calculate_completeness():
    user_ingredients = {'flour', 'sugar', 'butter', 'eggs'}
    recipe_ingredients = {'flour', 'sugar', 'milk', 'butter'}

    # Test for partial completeness
    assert calculate_completeness(user_ingredients, recipe_ingredients) == 75

    # Test for full completeness
    user_ingredients.add('milk')
    assert calculate_completeness(user_ingredients, recipe_ingredients) == 100

    # Test for zero completeness
    assert calculate_completeness(set(), recipe_ingredients) == 0

    # Test with no matching ingredients
    assert calculate_completeness({'rice', 'beans'}, recipe_ingredients) == 0
