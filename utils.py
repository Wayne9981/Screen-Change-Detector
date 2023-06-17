import logging
from functools import wraps
from time import time


def log_times(func):
    """decorator to log everything upon entry and exit of a function/method"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        mod_name = func.__module__
        logger = logging.getLogger(mod_name)
        logger.debug(
            f"Start {mod_name}.{func.__name__}: args={str(args)}, kwargs={str(kwargs)}"
        )
        now = time()
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"On exit {mod_name}.{func.__name__}: exception={str(e)}")
            raise
        else:
            logging.debug(
                f"Done {mod_name}.{func.__name__}: res={str(res)}, spend {time() - now} sec"
            )
            return res

    return wrapper
