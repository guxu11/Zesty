from apps.daos.userIngredient_dao import UserIngredientDAO
from apps.daos.ingredient_dao import IngredientDAO
from apps.daos.recipeIngredient_dao import RecipeIngredientDAO
from apps.enums.response_status import ResponseStatus
from apps.constants.constants import *
from apps.utils.decorators import *
from apps.common.transaction_processor import transactional

class UserIngredientService:
    def __init__(self):
        self.userIngredeint_dao = UserIngredientDAO()
        self.ingredient_dao = IngredientDAO()
        self.recipeIngredient_dao = RecipeIngredientDAO()

    @transactional(timeout=TRANSACtION_TIMEOUT)
    def batch_edit_userIngredients(self, input):
        user_id = input.get('userId')
        added_ingredients = input.get('added_ingredients')
        deleted_ingredients = input.get('deleted_ingredients')

        response = {}
        try:
            for ingredientName in added_ingredients:
                existingIngredient = self.ingredient_dao.get_ingredient_by_exact_name(ingredientName)
                if existingIngredient is None:
                    ingredientId = self.ingredient_dao.add_ingredient(ingredientName, 10000) # default category
                else:
                    ingredientId = existingIngredient.get('ingredientId')
                userIngredient = self.userIngredeint_dao.get_user_ingredient_by_ingredientId(ingredientId, user_id)
                if userIngredient is None:
                    self.userIngredeint_dao.add_user_ingredient(ingredientId, user_id)
                    print("added", ingredientName)
            for ingredientName in deleted_ingredients:
                ingredient = self.ingredient_dao.get_ingredient_by_exact_name(ingredientName)
                ingredientId = ingredient.get('ingredientId')
                self.userIngredeint_dao.delete_user_ingredient_by_id(ingredientId, user_id)
                print("deleted", ingredientName)
            response.update(UserIngredientResponseStatus.SUCCESS)
        except Exception as e:
            response.update(UserIngredientResponseStatus.FAIL)
            print(e)
        return response


    @transactional(timeout=TRANSACtION_TIMEOUT)
    def add_userIngredient(self, input):
        response = {}
        try:
            userId = input.get('userId')    
            ingredients = input.get('ingredients')
            
            for ingredient in ingredients:
                ingredientName = ingredient.get('ingredientName')
                category = ingredient.get('category')
                
            
                existingIngredient = self.ingredient_dao.get_ingredient_by_exact_name(ingredientName)
                if existingIngredient is None:
                    ingredientId = self.ingredient_dao.add_ingredient(ingredientName, category)
                else:
                    ingredientId = existingIngredient.get('ingredientId')
                
                userIngredient = self.userIngredeint_dao.get_user_ingredient_by_ingredientId(ingredientId, userId)

                if userIngredient is None:
                    self.userIngredeint_dao.add_user_ingredient(ingredientId, userId)


            response.update(UserIngredientResponseStatus.SUCCESS)
        except Exception as e:
            response.update(UserIngredientResponseStatus.FAIL)
            print(e)
        return response


    def delete_userIngredient_by_name(self, input):
        response = {}
        try:
            userId = input.get('userId')
            userIngredientName = input.get('userIngredientName')
            ingredient = self.ingredient_dao.get_ingredient_by_exact_name(userIngredientName)
            ingredientId = ingredient.get('ingredientId')
            self.userIngredeint_dao.delete_user_ingredient_by_id(ingredientId, userId)
            response.update(UserIngredientResponseStatus.SUCCESS)
        except Exception as e:
            response.update(UserIngredientResponseStatus.FAIL)
            print(e)
        return response
    

    def get_userIngredients(self, input):
        response = {}
        try:
            userId = input
            userIngredients = self.userIngredeint_dao.get_user_ingredients_by_userId(userId)
            userIngredientNames = []
            for userIngredient in userIngredients:
                userIngredientId = self.ingredient_dao.get_ingredient_by_id(userIngredient.get('ingredientId'))
                if userIngredientId is None:
                    continue
                userIngredientName = userIngredientId.get('ingredientName')
                # if userIngredientName is None:
                #     continue
                userIngredientNames.append(userIngredientName)
            if userIngredients is None:
                response.update(UserIngredientResponseStatus.NO_INGREDIENTS_FOUND)
                return response
            response.update({"data": userIngredientNames})
            print(userIngredientNames)
            response.update(UserIngredientResponseStatus.SUCCESS)
        except Exception as e:
            response.update(UserIngredientResponseStatus.FAIL)
            print(e)
        return response
    

    def get_missingIngredients(self, recipeId, userId):
        response = {}
        try:
            
            recipeIngredients = self.recipeIngredient_dao.get_ingredients_by_recipeId(recipeId)
            userIngredients = self.userIngredeint_dao.get_user_ingredients_by_userId(userId)

            recipeIngredients_id = set(ingredient['ingredientId'] for ingredient in recipeIngredients)
            userIngredients_id = set(ingredient['ingredientId'] for ingredient in userIngredients)
            missing_ingredients_id = recipeIngredients_id - userIngredients_id
            
            percent_difference = len(missing_ingredients_id) / len(recipeIngredients) * 100

            missing_ingredient_ids = [ingredient["ingredientId"] for ingredient in recipeIngredients if ingredient['ingredientId'] in missing_ingredients_id]

            miss_ingredients = self.ingredient_dao.get_ingredient_by_ids(missing_ingredient_ids)

            response.update({"data": {"missing_ingredients": miss_ingredients}})
            response["data"].update({"percent_incommon": 100-percent_difference}) 
            response.update(UserIngredientResponseStatus.SUCCESS)
        except Exception as e:
            response.update(UserIngredientResponseStatus.FAIL)
            print(e)

        return response
    

class UserIngredientResponseStatus(ResponseStatus):
       NO_INGREDIENTS_FOUND = {"statusCode": "100100", "statusMessage": "No userIngredients found"}