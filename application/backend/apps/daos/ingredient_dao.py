from apps import db
from apps.models.ingredient import Ingredient
from apps.common.search_engine import SearchEngine
from sqlalchemy import or_

class IngredientDAO:
    def __init__(self):
        self.searchEngine = SearchEngine()

    def get_ingredient_by_id(self, ingredientId):
        ingredient = db.session.query(Ingredient).filter(Ingredient.ingredientId == ingredientId).first()
        if ingredient is None:
            return None
        return ingredient.to_dict()

    def get_ingredient_by_ids(self, ingredientIds):
        ingredients = db.session.query(Ingredient).filter(Ingredient.ingredientId.in_(ingredientIds)).all()
        if ingredients is None:
            return None
        return [ingredient.to_dict() for ingredient in ingredients]

    def get_ingredients_by_name(self, ingredientName):
        print("starting get_ingredients_by_name inside ingredient DAO")
        ingredient = db.session.query(Ingredient).filter(Ingredient.ingredientName.like(f'%{self.searchEngine.extract_text(ingredientName)}%')).first()
        print("1a")
        if ingredient is None:
            return None
        return ingredient.to_dict()
    
    # used for user_ingredient_service
    def get_ingredient_by_exact_name(self, ingredientName):
        ingredient = db.session.query(Ingredient).filter(Ingredient.ingredientName == ingredientName).first()
        if ingredient is None:
            return None
        return ingredient.to_dict()

    def get_ingredients_by_names(self, ingredientNames):
        search_patterns = [f'%{self.searchEngine.extract_text(name)}%' for name in ingredientNames]
        query_conditions = [Ingredient.ingredientName.like(pattern) for pattern in search_patterns]
        ingredients = db.session.query(Ingredient).filter(or_(*query_conditions)).all()
        if not ingredients:
            return []
        return [ingredient.to_dict() for ingredient in ingredients]

    def add_ingredient(self, ingredientName, category):
        ingredient = Ingredient(
            ingredientName=ingredientName,
            category=category
        )
        db.session.add(ingredient)
        db.session.flush()
        return ingredient.ingredientId

    def add_ingredients(self, ingredients):
        ingredient_objects = [Ingredient(**data) for data in ingredients]
        db.session.add_all(ingredient_objects)
        db.session.flush()
        return [ingredient.ingredientId for ingredient in ingredient_objects]
