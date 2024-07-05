from apps import db
from apps.models.review import Review


class ReviewDAO:
    def __init__(self):
        pass

    def get_review_by_recipe(self, recipeId):
        review = db.session.query(Review).filter(Review.recipeId == recipeId).all()
        if review is None:
            return None
        return review
    
    def get_review_by_user(self, userId):
        review = db.session.query(Review).filter(Review.userId == userId).all()
        if review is None:
            return None
        return review
    
    def get_review_by_user_and_recipe(self, userId, recipeId):
        review = db.session.query(Review).filter(Review.userId == userId).filter(Review.recipeId == recipeId).first()
        if review is None:
            return None
        return review
    
    def add_review(self, userId, recipeId, comment, rating):
        if comment is None and rating is None:
            return None
        review = Review(userId=userId, recipeId=recipeId, comment=comment, rating=rating, status=1)
        db.session.add(review)
        db.session.commit()

    # the way this is made makes it so that an account can only have one review on a recipe
    # otherwise it'll delete all of the account's reviews on the recipe
    def update_review(self, userId, recipeId, comment, rating):
        review = db.session.query(Review).filter(Review.userId == userId).filter(Review.recipeId == recipeId).first()
        if review is None:
            return None
        review.comment = comment
        review.rating = rating
        db.session.commit()

    # probably works
    def get_avg_rating(self, recipeId):
        avg_rating = db.session.query(
            db.func.avg(Review.rating)).filter(Review.recipeId == recipeId).scalar()
        if avg_rating is None:
            return 5.0
        return round(avg_rating, 1)
        
    def get_avg_score_by_recipeId(self, recipeId):
        score = db.session.query(db.func.avg(Review.rating)).filter(Review.recipeId == recipeId).scalar()
        if score is None:
            return 5.0
        return round(score, 1)

    def get_avg_score_by_recipeIds(self, recipeIds):
        scores = db.session.query(
            Review.recipeId,
            db.func.avg(Review.rating)
        ).filter(
            Review.recipeId.in_(recipeIds)
        ).group_by(
            Review.recipeId
        ).all()

        # 创建一个字典，键是recipeId，值是平均评分或默认评分
        score_dict = {}
        for recipeId in recipeIds:
            # 找到对应的评分
            score = next((s for s in scores if s[0] == recipeId), None)
            # 如果找到了评分且评分不为None，则四舍五入并赋值，否则使用默认值
            score_dict[recipeId] = round(score[1], 1) if score and score[1] is not None else 5.0

        return score_dict