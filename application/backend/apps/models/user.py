from werkzeug.security import generate_password_hash, check_password_hash
from apps import db

class User(db.Model):
    __tablename__ = 'user'

    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(45), nullable=True, index=True)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    userType = db.Column(db.Integer, nullable=True)
    createTime = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    modifyTime = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # @property
    # def password(self):
    #     print('password is not a readable attribute')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):  
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != 'password'}
