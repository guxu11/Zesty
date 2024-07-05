from datetime import datetime
from apps import db
from apps.models.recipe import Recipe
from apps.common.search_engine import SearchEngine
from apps.constants.constants import HOMEPAGE_RECIPES_NUM
import random


class RecipeDAO:
    def __init__(self):
        self.searchEngine = SearchEngine()

    def get_recipe_by_id(self, recipeId):
        recipe = db.session.query(Recipe).filter(Recipe.recipeId == recipeId).first()
        if recipe is None:
            return None
        return recipe.to_dict()

    def get_recipes_by_name(self, recipeName):
        recipes = (
            db.session.query(Recipe)
            .filter(
                Recipe.recipeName.like(
                    f"%{self.searchEngine.extract_text(recipeName)}%"
                )
            )
            .all()
        )
        if recipes is None:
            return None
        return [recipe.to_dict() for recipe in recipes]

    def get_recipes_preview_by_id(self, recipeId):
        recipe = db.session.query(Recipe).filter(Recipe.recipeId == recipeId).first()
        if recipe is None:
            return None
        return recipe.to_preview_dict()

    def get_recipes_preview_by_creator(self, creatorId):
        recipes = db.session.query(Recipe).filter(Recipe.creatorId == creatorId).order_by(Recipe.modifyTime.desc()).all()
        if recipes is None:
            return None
        return [recipe.to_preview_dict() for recipe in recipes]

    def get_recipes_preview_by_name(self, recipeName):
        recipes = (
            db.session.query(Recipe)
            .filter(
                Recipe.recipeName.like(
                    f"%{self.searchEngine.extract_text(recipeName)}%"
                )
            )
            .all()
        )
        if recipes is None:
            return None
        return [recipe.to_preview_dict() for recipe in recipes]

    def add_recipe(
        self,
        recipeName,
        createorId,
        recipeType,
        category,
        difficulty,
        cookingTime,
        steps,
        recipePicture,
        status,
        description,
    ):
        recipe = Recipe(
            recipeName=recipeName,
            creatorId=createorId,
            recipeType=recipeType,
            category=category,
            difficulty=difficulty,
            cookingTime=cookingTime,
            steps=steps,
            recipePicture=recipePicture,
            status=status,
            description=description,
        )
        db.session.add(recipe)
        db.session.flush()
        return recipe.recipeId

    def get_random_recipes(self):
        count = db.session.query(db.func.count(Recipe.recipeId)).scalar()
        random_ids = random.sample(range(1, count + 1), HOMEPAGE_RECIPES_NUM)
        recipes = db.session.query(Recipe).filter(Recipe.recipeId.in_(random_ids)).all()
        return [recipe.to_dict() for recipe in recipes]
