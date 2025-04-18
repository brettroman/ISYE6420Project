import time
import functools
import inspect
from project.logger import logger

'''
    CREDIT: https://chatgpt.com
    I used ChatGPT to help me write these decorators.
'''

def time_function(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        module_name = get_module_name()

        logger.debug(f"{module_name} {func.__name__} executed in: {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        module_name = get_module_name()

        logger.debug(f"Calling {module_name}.{func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logger.debug(f"{module_name}.{func.__name__} returned: {result}")
        return result
    return wrapper

def handle_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            module_name = get_module_name()
            logger.critical(f"Unhandled error in {module_name}.{func.__name__}: {e}", exc_info=True)
            raise
    return wrapper

def get_module_name():
    frame = inspect.currentframe().f_back.f_back
    return frame.f_globals["__name__"]