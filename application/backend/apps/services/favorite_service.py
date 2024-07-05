from apps.daos.favorite_dao import FavoriteDAO
from apps.daos.recipe_dao import RecipeDAO
from apps.daos.review_dao import ReviewDAO
from apps.enums.response_status import ResponseStatus


class FavoriteService:
    def __init__(self):
        self.favorite_dao = FavoriteDAO()
        self.recipe_dao = RecipeDAO()
        self.review_dao = ReviewDAO()

    # add check for user and recipe
    def add_favorite(self, input):
        if input is None:
            return FavoriteResponse.FAIL
        userId = input.get("userId")
        recipeId = input.get("recipeId")
        status = input.get("status")
        to_status = 1 if status is None or status == 0 else 0
        favorite = self.favorite_dao.get_favorite_by_user_and_recipe(userId, recipeId)
        try:
            if favorite is not None:
                self.favorite_dao.change_favorite(favorite, to_status)
            else:
                self.favorite_dao.add_favorite(userId, recipeId)
            return FavoriteResponse.SUCCESS
        except Exception as e:
            print(e)
            return FavoriteResponse.FAIL

    def get_favorite_status(self, input):
        if input is None:
            return FavoriteResponse.FAIL
        userId = input.get("userId")
        recipeId = input.get("recipeId")
        response = {"data": {"status": 0}}
        try:
            favorite = self.favorite_dao.get_favorite_by_user_and_recipe(
                userId, recipeId
            )
            if favorite is not None:
                response["data"]["status"] = favorite.to_dict()["status"]
        except Exception as e:
            pass
        response.update(FavoriteResponse.SUCCESS)
        return response

    def get_user_favorites(self, input):
        if input is None:
            return FavoriteResponse.FAIL
        userId = input
        response = {}
        try:
            favorites = self.favorite_dao.get_favorite_by_user(userId)
            favorite_list = []
            for favorite in favorites:
                favorite_dict = favorite.to_dict()
                recipeId = favorite_dict["recipeId"]
                
                recipe = self.recipe_dao.get_recipes_preview_by_id(recipeId)

                if recipe is None:
                    continue
            
                favorite_dict["recipeName"] = (
                    recipe["recipeName"] if recipe is not None else "Unknown"
                )
                recipe_rating = self.review_dao.get_avg_score_by_recipeId(recipeId)
                if recipeId is None:
                    continue
                recipe["rating"] = recipe_rating
                favorite_list.append(recipe)
            response.update({"data": favorite_list})
        except Exception as e:
            print(e)
            return FavoriteResponse.FAIL
        response.update(FavoriteResponse.SUCCESS)
        return response


class FavoriteResponse(ResponseStatus):
    USER_NOT_EXIST = {"statusCode": 100100, "statusMessage": "User doesn't exist"}
    RECIPE_NOT_EXIST = {"statusCode": 100200, "statusMessage": "Recipie doesn't exist"}
