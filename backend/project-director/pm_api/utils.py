from django.conf import settings
from django.db import connection, reset_queries

from rest_framework.filters import BaseFilterBackend

from typing import Union

import random
import string
from functools import wraps



def track_queries(func):
    """
    If debug is true then count the number of queries executed inside 
    a function or method.
    """
    @wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
        if not settings.DEBUG:
            return func(*args, **kwargs)       
        result = func(*args, **kwargs)
        print(f"\nIn File: ||{func.__module__}|| Method: ||{func.__name__}|| {len(connection.queries)} queries were executed.\n")
        if len(connection.queries) <= 10:
            for i, q in enumerate(connection.queries):
                print(f"\n{i}: {q}\n")
        return result
    return inner_func


def rand_password(length=10) -> str:
    if settings.DEBUG:
        return "1234"
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))

def validate_request(data: dict, exceptions: list = []):
    #TODO this needs to be abstracted into a class for other views to use.
    for k, v in data.items():
        if v == None:
            if k not in exceptions:
                return k, False
    return None, True

def parse_params(request, model, additional_params: Union[set] = {}, required_params: Union[set, None] = None) -> dict:
    #TODO this needs to be abstracted into a class for other views to use.
    """
    Checks the query params against the models fields that they will used to filter for.
    If a param is not valid return the invalid param, False.
    """
    allowed_query_params = set(f.name for f in model._meta.get_fields()).union(additional_params)
    query_params = request.query_params.copy()
    #dont want to use the page parameter to filter
    #but need it for pagination
    query_params.pop("page", None)
    params: dict = {}
    if required_params is not None:
        #if there are required params take the intersection between the keys of
        #the request params and the required ones. If the set created from that
        #doesnt match the require params set size then a required param is missing.
        if len(set(query_params.keys()).intersection(required_params)) != len(required_params):
            return required_params, False
    if len(query_params) > 0:
        for k, v in query_params.items():
            if k == "pk":
                k = "id"
            if k == "date_created__date__gte" or k == "job_id":
                params[k] = v
                continue
            #TODO need to fix
            # elif k not in allowed_query_params:
            #     return k, False
            params[k] = v     
    return params, True