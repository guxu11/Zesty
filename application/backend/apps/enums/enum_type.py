from enum import Enum

class IngredientType(Enum):
    MEAT = 1
    VEGETABLE = 2
    FRUIT = 3
    GRAIN = 4
    DAIRY = 5
    OIL = 6
    SPICE = 7
    SWEETENER = 8
    LIQUID = 9
    NUT = 10
    SEAFOOD = 11
    EGG = 12
    SAUSE = 13
    OTHER = 10000

    @staticmethod
    def get_category_name_by_code(code):
        for type in IngredientType:
            if type.value == code:
                return type.name.capitalize()
        return IngredientType.OTHER.name.capitalize()

class RecipeCategory(Enum):
    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3
    DESSERT = 4
    SNACK = 5
    DRINK = 6
    OTHER = 10000

    @staticmethod
    def get_category_name_by_code(code):
        for category in RecipeCategory:
            if category.value == code:
                return category.name.capitalize()
        return RecipeCategory.OTHER.name.capitalize()
