from apps.daos.review_dao import ReviewDAO
from apps.enums.response_status import ResponseStatus

class ReviewService:
    def __init__(self):
        self.review_dao = ReviewDAO()


    # add check for user and recipe
    def add_review(self, userId, recipeId, comment, rating):
        response = {}
        review = self.review_dao.get_review_by_user_and_recipe(userId, recipeId)
        print(review)
        try:
            if comment is None and rating is None:
                response.update(ReviewResponse.No_Comment_Or_Rate)
                return response
            if review is not None: # if a review is already made it'll overwrite it
                print("updating")
                self.review_dao.update_review(userId, recipeId, comment, rating)
            else:
                self.review_dao.add_review(userId, recipeId, comment, rating)
            response.update(ReviewResponse.SUCCESS)
            return response
        except Exception as e:
            print(e)
            response.update(ReviewResponse.FAIL)
            return response

    def get_avg(self, recipeId):
        response = {}
        avg = self.review_dao.get_avg_rating(recipeId)
        response.update(ReviewResponse.SUCCESS)
        response.update({"data": avg})

        return response
 
         
class ReviewResponse(ResponseStatus):
    USER_NOT_EXIST = {"statusCode": 100100, "statusMessage": "User doesn't exist"} 
    RECIPE_NOT_EXIST = {"statusCode": 100200, "statusMessage": "Recipie doesn't exist"}
    No_Comment_Or_Rate = {"statusCode": 100300, "statusMessage": "Needs a comment or rating"}
	