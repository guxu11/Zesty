from apps import db
from apps.models.user import User

class UserDAO:
    def __init__(self):
        pass

    def get_user_by_id(self, userId):
        user = db.session.query(User).filter(User.userId == userId).first()
        if user is None:
            return None
        return user

    def get_user_by_email(self, email):
        user = db.session.query(User).filter(User.email == email).first()
        if user is None:
            return None
        return user

    def add_user(self, userName, email, password, userType=3):
        user = User(userName=userName, email=email, userType=userType)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()