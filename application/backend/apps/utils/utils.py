import random
import string
import time
import re
from typing import Optional

def gen_random_string(length=50):
    timestamp = str(int(time.time()))
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length)) + timestamp

def calculate_completeness(user_ingredient_ids, recipe_ingredient_ids):
    assert isinstance(user_ingredient_ids, set)
    assert isinstance(recipe_ingredient_ids, set)
    overlaps = user_ingredient_ids & recipe_ingredient_ids
    return len(overlaps) / len(recipe_ingredient_ids) * 100

def extract_code_from_markdown(markdown_text: str, language: Optional[str] = None) -> str:
    # Create a regular expression pattern for the specified language or for any language if not specified
    if language:
        code_block_pattern = re.compile(rf'```{language}\n(.*?)```|(?:^|\n)(.*?)(?=\n\S|\Z)', re.DOTALL)
    else:
        code_block_pattern = re.compile(r'```(?:[a-zA-Z]*)\n(.*?)```|(?:^|\n)(.*?)(?=\n\S|\Z)', re.DOTALL)

    # Find all code blocks matching the pattern in the markdown text
    code_blocks = code_block_pattern.findall(markdown_text)

    # Extract the code from the matched groups
    pure_code_list = []
    for block in code_blocks:
        if block[0]:  # If the first group matched (code block with markdown)
            pure_code_list.append(block[0])
        elif block[1]:  # If the second group matched (code block without markdown)
            lines = block[1].strip().split('\n')
            if all(line.strip() for line in lines):  # Ensure all lines have content
                pure_code_list.append(block[1])

    # Join all code blocks into a single string
    pure_code = "\n\n".join(pure_code_list)

    return pure_code

if __name__ == '__main__':
    text = '{"recipeTitle": "Thanksgiving Feast", "recipeDescription": "A traditional Thanksgiving dinner with all the trimmings.", "recipeIngredients": {"Roasted turkey": "1 (12-14 pound) turkey", "Stuffing": "8 cups", "Mashed potatoes": "5 pounds", "Gravy": "2 cups", "Cranberry sauce": "1 (14 ounce) can", "Green bean casserole": "1 (10.75 ounce) can", "Sweet potato casserole": "1 (15 ounce) can", "Rolls": "1 dozen", "Pumpkin pie": "1 (9 inch) pie"}, "recipeDifficulty": "Hard", "recipeInstructions": ["Preheat oven to 325 degrees F (165 degrees C).", "Remove giblets and neck from turkey cavity. Rinse turkey inside and out, and pat dry.", "Place turkey in a roasting pan. Rub skin with butter or olive oil, and season with salt and pepper.", "Fill turkey cavity with stuffing.", "Roast turkey in preheated oven for 3 to 4 hours, or until a meat thermometer inserted into the thickest part of the thigh registers 165 degrees F (74 degrees C).", "Let turkey rest for 10 minutes before carving.", "While turkey is roasting, prepare remaining dishes according to package directions.", "Serve turkey with stuffing, mashed potatoes, gravy, cranberry sauce, green bean casserole, sweet potato casserole, rolls, and pumpkin pie."]}'
    import json
    text_json = extract_code_from_markdown(text, "json")
    if text_json:
        print(json.loads(text_json))
    else:
        print("No JSON code block found in the text")