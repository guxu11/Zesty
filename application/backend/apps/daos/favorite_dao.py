from apps import db
from apps.models.favorite import Favorite
from sqlalchemy import and_


class FavoriteDAO:
    def __init__(self):
        pass
    
    def get_favorite_by_user(self, userId):
        favorite = db.session.query(Favorite).filter(
            Favorite.userId == userId,
            Favorite.status == 1
        ).order_by(Favorite.modifyTime.desc()).all()
        if not favorite:
            return None
        return favorite

    def get_favorite_by_user_and_recipe(self, userId, recipeId):
        favorite = db.session.query(Favorite).filter(and_(Favorite.userId == userId, Favorite.recipeId == recipeId)).first()
    
        if favorite is None:
            return None
        return favorite

    def add_favorite(self, userId, recipeId):
        favorite = Favorite(userId = userId, recipeId=recipeId, status=1)
        db.session.add(favorite)
        db.session.commit()

    def change_favorite(self, favorite, to_status):
        favorite.status = to_status
        db.session.commit()

