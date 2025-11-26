from time import time, ctime
from functools import wraps


def log(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time()
            try:
                result = func(*args, **kwargs)
                end_time = time()
                duration = end_time - start_time
                log_message = f"[{ctime()}] {func.__name__} ok (duration: {duration:.4f}s)"

                _write_log(log_message, filename)
                return result

            except Exception as e:
                end_time = time()
                duration = end_time - start_time
                error_type = type(e).__name__
                inputs_str = f"Inputs: {args}, {kwargs}"
                log_message = (f"[{ctime()}] {func.__name__} error: {error_type}. {inputs_str} "
                               f"(duration: {duration:.4f}s)")

                _write_log(log_message, filename)
                raise

        return wrapper
    return decorator
def _write_log(message, filename):
    """Вспомогательная функция для записи лога в файл или консоль."""
    if filename:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
    else:
        print(message)

@log(filename="mylog.txt")
#Вывод в файл
def my_function(x, y):
    return x + y

my_function(1, 2)


@log()
#Вывод в консоль
def my_function(x, y):
    return x + y

my_function(1, 2)