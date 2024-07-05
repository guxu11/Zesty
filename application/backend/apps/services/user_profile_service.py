from apps.daos.user_dao import UserDAO
from apps.daos.recipe_dao import RecipeDAO
from apps.daos.review_dao import ReviewDAO
from apps.enums.response_status import ResponseStatus


class UserProfileService:
    def __init__(self):
        self.user_dao = UserDAO()
        self.recipe_dao = RecipeDAO()
        self.review_dao = ReviewDAO()

    def register(self, name, email, password):
        response = {}
        try:
            user = self.user_dao.get_user_by_email(email)
            if user is not None:
                response.update(RegisterResponse.EMAIL_EXIST)
            else:
                user = self.user_dao.add_user(name, email, password)
                response.update(RegisterResponse.SUCCESS)
        except Exception as e:
            print(e)
            response.update(RegisterResponse.FAIL)
        return response

    def login(self, email, password):
        response = {}
        try:
            user = self.user_dao.get_user_by_email(email)
            if user is None:
                response.update(LoginResponse.USER_NOT_EXIST)
            elif user.verify_password(password):
                response.update(LoginResponse.SUCCESS)
                response.update({"data": user.to_dict()})
            else:
                return LoginResponse.WRONG_PASSWORD
        except Exception as e:
            print(e)
            response.update(LoginResponse.FAIL)
        return response

    def get_posted_recipes(self, input):
        if input is None:
            return ResponseStatus.FAIL
        userId = input
        response = {}
        try:
            posted = self.recipe_dao.get_recipes_preview_by_creator(userId)
            posted_list = []
            for post in posted:
                recipeId = post["recipeId"]
                recipe_rating = self.review_dao.get_avg_score_by_recipeId(recipeId)
                post["rating"] = recipe_rating
                posted_list.append(post)
            response.update({"data": posted_list})
        except Exception as e:
            print(e)
            return ResponseStatus.FAIL
        response.update(ResponseStatus.SUCCESS)
        return response


class RegisterResponse(ResponseStatus):
    EMAIL_EXIST = {"statusCode": 100100, "statusMessage": "Email already exists"}


class LoginResponse(ResponseStatus):
    USER_NOT_EXIST = {"statusCode": 100100, "statusMessage": "User doesn't exist"}
    WRONG_PASSWORD = {"statusCode": 100200, "statusMessage": "Wrong password"}
