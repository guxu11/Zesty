from apps import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class UserIngredient(db.Model):
    __tablename__ = 'userIngredient'

    userIngredientId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredientId = db.Column(db.Integer, nullable=True, index=True)
    userId = db.Column(db.Integer, nullable=True, index=True)
    createTime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modifyTime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('userId', 'ingredientId', name='user_ingredient_idx'),
    )

    def to_dict(self):
        return {
            'userIngredientId': self.userIngredientId,
            'ingredientId': self.ingredientId,
            'userId': self.userId,
            'createTime': self.createTime.isoformat(),
            'modifyTime': self.modifyTime.isoformat(),
        }
