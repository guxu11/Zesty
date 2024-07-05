from functools import wraps

def response_builder(key: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            original_result = func(*args, **kwargs)
            return {
                "responseCode": 200,
                "responseMessage": "OK",
                key: original_result
            }
        return wrapper
    return decorator

@response_builder('result')
def example_function():
    return [1, 2, 3]
