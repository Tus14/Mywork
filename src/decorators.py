from time import time, ctime
from functools import wraps
import os
from typing import Callable, Optional, Any


DecoratorFunction = Callable[..., Any]


def log(filename: Optional[str] = None) -> Callable[[DecoratorFunction], DecoratorFunction]:
    """Декоратор, который будет автоматически логировать начало и конец выполнения функции,
     а также ее результаты или возникшие ошибки"""
    def decorator(func: DecoratorFunction) -> DecoratorFunction:
        """Функция-декоратор"""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Функция-обертка"""
            start_time: float = time()
            log_message: str
            result: Any
            end_time: float
            duration: float
            try:
                result = func(*args, **kwargs)
                end_time = time()
                duration = end_time - start_time
                log_message = f"[{ctime()}] {func.__name__} ok (duration: {duration:.6f}s)"

            except Exception as e:
                end_time = time()
                duration = end_time - start_time
                error_type: str = type(e).__name__
                inputs_str: str = f"Inputs: {args}, {kwargs}"
                log_message = (
                    f"[{ctime()}] {func.__name__} error: {error_type}. {inputs_str} " f"(duration: {duration:.6f}s)"
                )

                raise
            finally:
                # Этот блок выполняется и при успешном выполнении, и при ошибке (до raise)
                if log_message:
                    _write_log(log_message, filename)
            return result

        return wrapper  # type: ignore [return-value]

    return decorator


def _write_log(message: str, filename: Optional[str]) -> None:
    """Вспомогательная функция для записи лога в файл или консоль."""
    if filename:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)


@log(filename="mylog.txt")
# Вывод в файл
def my_function(x: int, y: int) -> int:
    return x + y


@log()
# Вывод в консоль
def my_function_console(x: float, y: float) -> float:
    return x + y
