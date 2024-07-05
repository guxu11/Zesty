from apps import db
from datetime import datetime
from apps.enums.enum_type import RecipeCategory
from sqlalchemy import Text

class Recipe(db.Model):
    __tablename__ = 'recipe'

    recipeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creatorId = db.Column(db.Integer, nullable=True)
    recipeName = db.Column(db.String(255), nullable=False)
    recipeType = db.Column(db.Integer, nullable=True)
    category = db.Column(db.Integer, nullable=True) 
    difficulty = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=True)
    postTime = db.Column(db.DateTime, nullable=True)
    steps = db.Column(db.JSON, nullable=True)
    cookingTime = db.Column(db.String(255), nullable=True)
    createTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modifyTime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    recipePicture = db.Column(db.String(2048), nullable=True)
    description = db.Column(Text, nullable=True)

    def to_dict(self):
        return {
            'recipeId': self.recipeId,
            'creatorId': self.creatorId,
            'recipeName': self.recipeName,
            'recipeType': self.recipeType,
            'category': RecipeCategory.get_category_name_by_code(self.category),
            'difficulty': self.difficulty,
            'status': self.status,
            'postTime': str(self.postTime),  
            'steps': self.steps,
            'cookingTime': self.cookingTime,
            'createTime': str(self.createTime),  
            'modifyTime': str(self.modifyTime), 
            'recipePicture': self.recipePicture,
            'description': self.description
        }
    def to_preview_dict(self):
        return {
            'recipeId': self.recipeId,
            'creatorId': self.creatorId,
            'recipeName': self.recipeName,
            'recipeType': self.recipeType,
            'category': RecipeCategory.get_category_name_by_code(self.category),
            'status': self.status,
            'postTime': str(self.postTime),  
            'createTime': str(self.createTime),  
            'modifyTime': str(self.modifyTime), 
            'recipePicture': self.recipePicture
        }
    