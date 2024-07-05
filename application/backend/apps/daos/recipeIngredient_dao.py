from apps import db
from apps.models.recipeIngredient import RecipeIngredient

class RecipeIngredientDAO:
    def __init__(self):
        pass
    def get_recipeIngredient_by_id(self, recipeIngredientId):
        recipeIngredient = db.session.query(RecipeIngredient).filter(RecipeIngredient.recipeIngredientId == recipeIngredientId).first()
        if recipeIngredient is None:
            return None
        return recipeIngredient.to_dict()

    def get_ingredients_by_recipeId(self, recipeId):
        recipeIngredients = db.session.query(RecipeIngredient).filter(RecipeIngredient.recipeId == recipeId).all()
        if recipeIngredients is None:
            return None
        return [recipeIngredient.to_dict() for recipeIngredient in recipeIngredients]
    
    def get_ingredients_by_ingredientId(self, ingredientId):
        recipeIngredients = db.session.query(RecipeIngredient).filter(RecipeIngredient.ingredientId == ingredientId).all()
        if recipeIngredients is None:
            return None
        return [recipeIngredient.to_dict() for recipeIngredient in recipeIngredients]
    
    def get_recipeIngredients_by_recipeId_ingredientId(self, recipeId, ingredientId):
        recipeIngredient = db.session.query(RecipeIngredient).filter(RecipeIngredient.recipeId == recipeId, RecipeIngredient.ingredientId == ingredientId).first()
        if recipeIngredient is None:
            return None
        return recipeIngredient.to_dict()

    def add_recipeIngredient(self, recipeId, ingredientId, amount):
        recipeIngredient = RecipeIngredient(
            recipeId=recipeId,
            ingredientId=ingredientId,
            amount=amount
        )
        db.session.add(recipeIngredient)
        return recipeIngredient.recipeIngredientId

    def add_recipeIngredients(self, recipeId, ingredients):
        recipeIngredient_objects = [RecipeIngredient(recipeId=recipeId, **data) for data in ingredients]
        db.session.add_all(recipeIngredient_objects)
        return [recipeIngredient.recipeIngredientId for recipeIngredient in recipeIngredient_objects]