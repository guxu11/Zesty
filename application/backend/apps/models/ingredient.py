from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from apps import db


class Ingredient(db.Model):
    __tablename__ = 'ingredient'

    ingredientId = db.Column(db.Integer, primary_key=True)
    ingredientName = db.Column(db.String(255), nullable=False, index=True)
    category = db.Column(db.Integer, nullable=True)
    createTime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modifyTime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    nutrition = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            'ingredientId': self.ingredientId,
            'ingredientName': self.ingredientName,
            'category': self.category,
            'createTime': self.createTime.isoformat(),
            'modifyTime': self.modifyTime.isoformat(),
            'nutrition': self.nutrition
        }
