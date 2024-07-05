from apps import app, db
from apps.services.recipe_service import RecipeService
from apps.services.user_profile_service import UserProfileService
from apps.services.recipe_service import RecipeService
from apps.services.review_service import ReviewService
from apps.services.user_ingredient_service import UserIngredientService
from apps.services.favorite_service import FavoriteService
from apps.services.file_upload_service import FileUploadService
from apps.services.gemini_service import GeminiService
from sqlalchemy.sql import text
from flask import request, jsonify
from apps.services.file_upload_service import *

recipe_service = RecipeService()
userProfileService = UserProfileService()
file_upload_service = FileUploadService()
favorite_service = FavoriteService()
review_service = ReviewService()
user_ingredeint_service = UserIngredientService()
gemini_service = GeminiService()



@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/check")
def check_db_connection():
    try:
        # Attempt to execute a simple database query to check the connection
        db.session.execute(text("SELECT 1"))
        return "Connected to the database!"
    except Exception as e:
        return f"Failed to connect to the database: {str(e)}"


@app.route("/api/recipe/<recipeId>")
def get_recipe_detail_by_id(recipeId):
    recipe = recipe_service.get_recipe_detail_by_id(recipeId)
    return jsonify(recipe)


# /api/recipe/search?q=chicken%20egg
@app.route("/api/recipe/search")
def search_recipes_by_keywords():
    input = request.args.get("q")
    response = recipe_service.search_recipes_preview_by_input_list(input)
    return jsonify(response)


@app.route("/api/user/register", methods=["POST"])
def register_user():
    data = request.get_json()
    # Process the registration data
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    response = userProfileService.register(name, email, password)
    return jsonify(response)


@app.route("/api/user/login", methods=["POST"])
def login_user():
    data = request.get_json()
    # Process the login data
    email = data.get("email")
    password = data.get("password")
    print(f"Email: {email}, Password: {password}")
    response = userProfileService.login(email, password)
    return jsonify(response)


@app.route("/api/recipe/create", methods=["POST"])
def create_recipe():
    data = request.get_json()
    response = recipe_service.createRecipe(data)
    return jsonify(response)


@app.route("/api/recipe/random")
def get_random_recipes():
    response = recipe_service.get_random_recipes()
    return jsonify(response)


@app.route("/api/recipe/upload", methods=["POST"])
def upload_img():
    img = request.files["file"]
    response = file_upload_service.upload_img(img)
    return jsonify(response)


@app.route("/api/recipe/favorite", methods=["POST"])
def create_favorite():
    data = request.get_json()
    response = favorite_service.add_favorite(data)
    return jsonify(response)


@app.route("/api/recipe/review", methods=["POST"])
def review_recipe():
    data = request.get_json()

    userId = data.get("userId")
    recipeId = data.get("recipeId")
    comment = data.get("comment")
    rating = data.get("rating")
    response = review_service.add_review(userId, recipeId, comment, rating)
    return jsonify(response)


@app.route("/api/recipe/favorite/status", methods=["POST"])
def get_favorite_status():
    data = request.get_json()
    response = favorite_service.get_favorite_status(data)
    return jsonify(response)

@app.route("/api/user/useringredients/edit", methods=["POST"])
def edit_user_ingredients():
    data = request.get_json()
    response = user_ingredeint_service.batch_edit_userIngredients(data)
    return jsonify(response)

@app.route('/api/ingredient/adduseringredient', methods=['POST'])
def add_userIngredient():
    data = request.get_json()
    response = user_ingredeint_service.add_userIngredient(data)
    return jsonify(response)


@app.route('/api/ingredient/deleteuseringredient', methods=['POST'])
def delete_userIngredient():
    data = request.get_json()
    print(data)
    response = user_ingredeint_service.delete_userIngredient_by_name(data)
    return jsonify(response)



@app.route("/api/user/userIngredients/<userId>")
def get_user_ingredients(userId):
    """Request for ingredients in user pantry"""
    response = user_ingredeint_service.get_userIngredients(userId)
    return jsonify(response)


@app.route("/api/recipe/<recipeId>/<userId>/missingingredients")
def get_missingingredients(recipeId, userId):
    """Request for recipe ingredients not in user pantry"""
    response = user_ingredeint_service.get_missingIngredients(recipeId, userId)
    return jsonify(response)


@app.route("/api/recipe/pantry/<userId>")
def get_pantry_recipe(userId):
    """Request for recipe search using user pantry ingredients"""

    response = recipe_service.get_recipes_by_pantry(userId)
    return jsonify(response)
  
@app.route("/api/user/<userId>/favorite", methods=["GET"])
def get_user_favorites(userId):

    response = favorite_service.get_user_favorites(userId)
    return jsonify(response)


  
@app.route("/api/user/<userId>/recipes", methods=["GET"])
def get_user_recipes(userId):
    """Request for recipes by user id"""
    response = userProfileService.get_posted_recipes(userId)
    return jsonify(response)



@app.route("/api/detect/ingredient", methods=["POST"])
def detect_ingredient():
    data = request.get_json()
    img_url = data.get("img_data")
    if img_url:
        # Call the appropriate function with the 'img_url'
        response = gemini_service.detect_ingredient(img_url)
    else:
        # Handle the case when 'img_url' is not present
        response = {"error": "No 'img_url' found in the request"}

    # Return the response as JSON
    return jsonify(response)


@app.route("/api/generate/recipes", methods=["POST"])
def generate_recipes():
    data = request.get_json()
    img_url = data.get("img_url")
    if img_url:
        # Call the appropriate function with the 'img_url'
        response = gemini_service.generate_recipe(img_url)
    else:
        # Handle the case when 'img_url' is not present
        response = {"error": "No 'img_url' found in the request"}

    # Return the response as JSON
    return jsonify(response)


