from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from apps import db

class Favorite(db.Model):
    __tablename__ = 'favorite'

    favoriteId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, nullable=True, index=True)
    recipeId = db.Column(db.Integer, nullable=True, index=True)
    status = db.Column(db.Integer, nullable=True)
    createTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modifyTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'favoriteId': self.favoriteId,
            'userId': self.userId,
            'recipeId': self.recipeId,
            'status': self.status,
            'createTime': self.createTime.isoformat(),
            'modifyTime': self.modifyTime.isoformat(),
        }
