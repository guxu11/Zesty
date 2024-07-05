from random import shuffle
from apps.daos.ingredient_dao import IngredientDAO
from apps.daos.recipe_dao import RecipeDAO
from apps.daos.review_dao import ReviewDAO
from apps.daos.recipeIngredient_dao import RecipeIngredientDAO
from apps.daos.user_dao import UserDAO
from apps.daos.userIngredient_dao import UserIngredientDAO
from apps.utils.decorators import *
from apps.utils.utils import *
from apps.enums.response_status import ResponseStatus
from apps.constants.constants import *
from apps.common.transaction_processor import transactional

class RecipeService:
    def __init__(self):
        self.recipe_dao = RecipeDAO()
        self.ingredient_dao = IngredientDAO()
        self.recipe_ingredient_dao = RecipeIngredientDAO()
        self.review_dao = ReviewDAO()
        self.user_dao = UserDAO()
        self.user_ingredient_dao = UserIngredientDAO()
    
    def get_recipe_detail_by_id(self, recipeId):
        response = {}
        try:
            recipe = self.recipe_dao.get_recipe_by_id(recipeId)
            if recipe is None:
                response.update(RecipeDetailResponseStatus.RECIPE_NOT_FOUND)
                response["statusMessage"] = response["statusMessage"].format(recipeId)
            else:
                recipe['rating'] = float(self.review_dao.get_avg_score_by_recipeId(recipeId))
                recipe_ingredient = self.recipe_ingredient_dao.get_ingredients_by_recipeId(recipeId)
                ingredient_ids = [recipe_ingredient['ingredientId'] for recipe_ingredient in recipe_ingredient]
                amounts = [recipe_ingredient['amount'] for recipe_ingredient in recipe_ingredient]
                recipe['ingredients'] = [self.ingredient_dao.get_ingredient_by_id(ingredient_id) for ingredient_id in ingredient_ids]
                for i in range(len(recipe['ingredients'])):
                    recipe['ingredients'][i]['amount'] = amounts[i]
                reviews = self.review_dao.get_review_by_recipe(recipeId)
                review_list = []
                for review in reviews:
                    review_dict = review.to_dict()
                    userId = review_dict['userId']
                    user = self.user_dao.get_user_by_id(userId)
                    review_dict['userName'] = user.to_dict()['userName'] if user is not None else "Unknown"
                    review_list.append(review_dict)
                recipe['reviews'] = review_list
                response.update(SearchResponseStatus.SUCCESS)
                response.update({"data": recipe})
        except Exception as e:
            response.update(SearchResponseStatus.FAIL)
            print(e)
        return response
    

    # @response_builder("recipes_preview")
    def search_recipes_preview_by_ingredient(self, ingredientName):
        # Get the ingredient by name
        ingredient = self.ingredient_dao.get_ingredients_by_name(ingredientName)
        if ingredient is None:
            return []
        print(ingredient)
        # Get the recipe ingredients by ingredient id
        recipe_ingredients = self.recipe_ingredient_dao.get_ingredients_by_ingredientId(int(ingredient['ingredientId']))
        if recipe_ingredients is None:
            return []
        # Get the recipes by recipe id
        recipes = [self.recipe_dao.get_recipes_preview_by_id(recipe_ingredient['recipeId']) for recipe_ingredient in recipe_ingredients]
        return recipes
    
    # @response_builder("recipes_preview")
    def search_recipes_preview_by_keywords(self, keyword):
        return self.recipe_dao.get_recipes_preview_by_name(keyword)
    
    # @response_builder("recipes_preview")
    def search_recipes_preview_by_ingredient_and_keywords(self, ingredientName, keyword):
        recipes_by_ingredient = self.search_recipes_preview_by_ingredient(ingredientName)
        recipes_by_keywords = self.search_recipes_preview_by_keywords(keyword)
        return list(set(recipes_by_ingredient) & set(recipes_by_keywords))
    
    # @response_builder("recipes_preview")
    def search_recipes_preview_by_input_list(self, input):
        response = {}
        recipes = []
        deduplicate = {}
        try:
            inputs = input.strip().split(',')
            if inputs:
                for item in inputs:
                    recipes_by_ingredients = self.search_recipes_preview_by_ingredient(item)
                    recipes_by_ingredients = [recipe for recipe in recipes_by_ingredients if recipe is not None]
                    recipes_by_keywords = self.search_recipes_preview_by_keywords(item)
                    recipes_by_keywords = [recipe for recipe in recipes_by_keywords if recipe is not None]
                    if recipes_by_ingredients or len(recipes_by_ingredients) > 0:
                        deduplicate.update({recipe['recipeId']: recipe for recipe in recipes_by_ingredients if recipe is not None})
                    if recipes_by_keywords or len(recipes_by_keywords) > 0:
                        deduplicate.update({recipe['recipeId']: recipe for recipe in recipes_by_keywords if recipe is not None})
                recipe_ids = list(deduplicate.keys())
                recipe_ratings = self.review_dao.get_avg_score_by_recipeIds(recipe_ids)
                for recipe_id in recipe_ids:
                    recipe = deduplicate[recipe_id]
                    recipe['rating'] = recipe_ratings[recipe_id]
                    recipes.append(recipe)
            response.update({"data": recipes})
            response.update(SearchResponseStatus.SUCCESS)
        except Exception as e:
            response.update(SearchResponseStatus.FAIL)
            print(e)
        return response
    
    @transactional(timeout=TRANSACtION_TIMEOUT)
    def createRecipe(self, input):
        response = {}
        try:
            creatorId, recipeName, category, recipePicture, cookingTime, recipeType, difficulty, ingredients, steps, description = input['userId'], input['recipeName'], input['category'], input['recipePicture'], input['cookingTime'], input['recipeType'], input['difficulty'], input['ingredients'], input['steps'], input['description']
            # insert recipe and get recipeId (status=Created)
            recipeId = self.recipe_dao.add_recipe(recipeName, creatorId, recipeType, category, difficulty, cookingTime, steps, recipePicture, 1, description)
            # insert ingredients into ingredient and get ingredientId
            ingredientId_amount_list = []
            for ingredient in ingredients:
                id_amount_map = {"amount": ingredient["amount"]}
                ingredientExist = self.ingredient_dao.get_ingredients_by_name(ingredient['name'])
                ingredientId = ingredientExist["ingredientId"] if ingredientExist is not None else self.ingredient_dao.add_ingredient(ingredient['name'], ingredient['category'])
                id_amount_map["ingredientId"] = ingredientId
                ingredientId_amount_list.append(id_amount_map)
            # insert recipeIngredient
            self.recipe_ingredient_dao.add_recipeIngredients(recipeId, ingredientId_amount_list)
            response.update(CreateRecipeResponseStatus.SUCCESS)
            response.update({"data": {"recipeId": recipeId}})
        except Exception as e:
            response.update(CreateRecipeResponseStatus.FAIL)
            print(e)
        return response
    
    def get_random_recipes(self):
        response = {}
        try:
            random_recipes = self.recipe_dao.get_random_recipes()
            recipe_ids = [recipe['recipeId'] for recipe in random_recipes]
            recipe_ratings = self.review_dao.get_avg_score_by_recipeIds(recipe_ids)
            for recipe in random_recipes:
                recipe['rating'] = recipe_ratings[recipe['recipeId']]
            # shuffle the recipes
            shuffle(random_recipes)
            response.update(SearchResponseStatus.SUCCESS)
            response.update({"data": random_recipes})
        except Exception as e:
            response.update(SearchResponseStatus.FAIL)
            print(e)
        return response

    def get_recipes_by_pantry(self, userId):
        response = {}
        try:
            user_ingredients = self.user_ingredient_dao.get_user_ingredients_by_userId(userId)
            if user_ingredients is None:
                return PantryRecipesResponseStatus.NO_INGREDIENTS
            # user's ingredient ids
            ingredient_ids = set([user_ingredient['ingredientId'] for user_ingredient in user_ingredients])
            deduplicated = set([])
            completeness = 0
            for ingredient_id in ingredient_ids:
                recipe_ingredients = self.recipe_ingredient_dao.get_ingredients_by_ingredientId(ingredient_id)
                if recipe_ingredients is None:
                    continue
                recipe_ids = [recipe_ingredient['recipeId'] for recipe_ingredient in recipe_ingredients]
                deduplicated.update(recipe_ids)
            if len(deduplicated) == 0:
                return PantryRecipesResponseStatus.NO_RECIPES_MATCHED_PANTRY
            recipe_ids = list(deduplicated)
            recipes = []
            for recipe_id in recipe_ids:
                recipe_preview = self.recipe_dao.get_recipes_preview_by_id(recipe_id)
                if recipe_preview is None:
                    continue
                recipe_ingredient_ids = [recipe_ingredient["ingredientId"] for recipe_ingredient in self.recipe_ingredient_dao.get_ingredients_by_recipeId(recipe_id)]
                completeness = calculate_completeness(ingredient_ids, set(recipe_ingredient_ids))
                recipe_preview['completeness'] = completeness
                recipes.append(recipe_preview)
            # sort the recipes by completeness
            recipes.sort(key=lambda x: x['completeness'], reverse=True)
            recipe_ratings = self.review_dao.get_avg_score_by_recipeIds(recipe_ids)
            for recipe in recipes:
                recipe['rating'] = recipe_ratings[recipe['recipeId']]
            response.update(SearchResponseStatus.SUCCESS)
            response.update({"data": recipes})
        except Exception as e:
            response.update(SearchResponseStatus.FAIL)
            print(e)
        return response


class SearchResponseStatus(ResponseStatus):
    pass

class RecipeDetailResponseStatus(ResponseStatus):
    RECIPE_NOT_FOUND = {"statusCode": "100100", "statusMessage": "Recipe id = {} not found."}

class CreateRecipeResponseStatus(ResponseStatus):
    pass

class PantryRecipesResponseStatus(ResponseStatus):
    NO_INGREDIENTS = {"statusCode": "100200", "statusMessage": "No ingredients found for user"}
    NO_RECIPES_MATCHED_PANTRY = {"statusCode": "100201", "statusMessage": "No recipes matched the pantry ingredients."}