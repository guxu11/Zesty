from sqlalchemy import Text
from datetime import datetime
from apps import db

class Review(db.Model):
    __tablename__ = 'review'

    reviewId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, nullable=True, index=True)  # 假设关联 User 表
    recipeId = db.Column(db.Integer, nullable=True, index=True)  # 假设关联 Recipe 表
    comment = db.Column(Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=True)
    createTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modifyTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'reviewId': self.reviewId,
            'userId': self.userId,
            'recipeId': self.recipeId,
            'comment': self.comment,
            'rating': self.rating,
            'status': self.status,
            'createTime': self.createTime.isoformat(),
            'modifyTime': self.modifyTime.isoformat(),
        }
