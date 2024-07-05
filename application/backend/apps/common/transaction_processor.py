import functools
from sqlalchemy.exc import SQLAlchemyError
from apps import db 


def transactional(timeout=None):
    """A decorator to add transactional support to functions."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                db.session.begin()
                result = func(*args, **kwargs)
                db.session.commit()
                return result
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f"An error occurred: {e}")
                raise
            except Exception as e:
                db.session.rollback()
                print(f"An unexpected error occurred: {e}")
                raise
        return wrapper
    return decorator
