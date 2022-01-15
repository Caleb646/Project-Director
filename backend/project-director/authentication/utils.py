from django.db import connection, reset_queries
from django.conf import settings

from functools import wraps

def track_queries(func):
    """
    If debug is true then count the number of queries executed inside a function or method.
    """
    @wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
        if not settings.DEBUG:
            return func(*args, **kwargs)       
        result = func(*args, **kwargs)
        print(f"\nIn File: ||{func.__module__}|| Method: ||{func.__name__}|| {len(connection.queries)} queries were executed.\n")
        return result
    return inner_func