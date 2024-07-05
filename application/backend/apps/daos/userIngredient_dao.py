from apps import db
from apps.models.userIngredient import UserIngredient

class UserIngredientDAO:
    def __init__(self):
        pass
    
    def add_user_ingredient(self, ingredientId, userId):
        userIngredient = UserIngredient(
            ingredientId = ingredientId,
            userId = userId
        )
        db.session.add(userIngredient)
        db.session.flush()

        return userIngredient.ingredientId
    
    
    def delete_user_ingredient_by_id(self, ingredientId, userId):
        userIngredient = db.session.query(UserIngredient).filter(UserIngredient.ingredientId == ingredientId, UserIngredient.userId == userId).first()

        if userIngredient is None:
            return None
        db.session.delete(userIngredient)
        db.session.commit()



    def get_user_ingredients_by_userId(self, userId):
        userIngredients = db.session.query(UserIngredient).filter(UserIngredient.userId == userId).all()

        if userIngredients is None:
            return None
        
        return [userIngredient.to_dict() for userIngredient in userIngredients]
    

    def get_user_ingredient_by_ingredientId(self, ingredientId, userId):
        userIngredientId = db.session.query(UserIngredient).filter(UserIngredient.ingredientId == ingredientId, UserIngredient.userId == userId).first()

        if userIngredientId is None:
            return None
        
        return userIngredientId