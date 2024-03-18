from functools import wraps
from flask import Flask

def log_function_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args[0].logger.info(f"Executando {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
