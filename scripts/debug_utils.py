import functools
import numpy as np
import pandas as pd

def get_value_str(value):
    if isinstance(value, np.ndarray):
        return "ndarray"
    elif isinstance(value, pd.DataFrame):
        return "DataFrame"
    else:
        return str(value)

def debug_args(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        outputs = f"{func.__name__}("
        for i, arg in enumerate(args, 1):
            outputs += f"{get_value_str(arg)}, "
        for key, value in kwargs.items():
            outputs += f"{key}': {get_value_str(value)}, "
        outputs += ")"
        print(outputs)

        return func(*args, **kwargs)

    return wrapper
