from datetime import datetime
from apps import db

class RecipeIngredient(db.Model):
    __tablename__ = 'recipeIngredient'

    recipeIngredientId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredientId = db.Column(db.Integer, index=True)
    recipeId = db.Column(db.Integer, index=True)
    amount = db.Column(db.String(255))
    createTime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modifyTime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'recipeIngredientId': self.recipeIngredientId,
            'ingredientId': self.ingredientId,
            'recipeId': self.recipeId,
            'amount': self.amount,
            'createTime': self.createTime.isoformat(),
            'modifyTime': self.modifyTime.isoformat(),
        }
