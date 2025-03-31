from functools import wraps

__version__ = '0.1'

DEBUG = True

def show_details(func):
    def wrapper(*args, **kwargs):

        if DEBUG:
            print(f"{func.__name__}: started with params {args[1:]=}, {kwargs=}")

        try:
            result = func(*args, *kwargs)
            if [] in result:
                raise ValueError(f'empty list in {result}')
        except Exception as e:
            print(f'{func.__name__}: processing error {e=}')
            raise e

        if DEBUG:
            print(f"{func.__name__}: finished with results {result}")
        return result
    return wrapper
