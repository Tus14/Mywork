import pytest
from src.decorators import log


def test_log_to_file_success(tmp_path):
    """Проверяет успешное выполнение функции и запись лога в файл."""
    # Подготовка: Создаем временный файл error_log.txt для работы в различных ос
    log_filename = tmp_path / "error_log.txt"
    filename_str = str(log_filename)
    @log(filename=filename_str)
    def failing_function(a, b):
        raise ValueError("Something went wrong")
    with pytest.raises(ValueError, match="Something went wrong"):
        failing_function(1, 0)
    assert log_filename.exists()
    content = log_filename.read_text(encoding='utf-8')
    assert "failing_function error: ValueError." in content
    assert "Inputs: (1, 0), {}" in content
    assert "(duration:" in content


def test_log_to_console_success(capsys):
    """Проверяет вывод лога успешного выполнения функции в консоль."""

    @log(filename=None)
    def console_function(x):
        return x * 2
    result = console_function(10)
    assert result == 20
    # Перехватываем вывод консоли (stdout и stderr)
    captured = capsys.readouterr()
    # Проверяем, что сообщение было напечатано в стандартный вывод (stdout)
    assert "console_function ok (duration:" in captured.out
    assert captured.err == ""


def test_log_to_console_exception(capsys):
    """Проверяет вывод лога ошибки в консоль при возникновении исключения."""

    @log()
    def console_failing_function():
        raise TypeError("Bad type")
    with pytest.raises(TypeError, match="Bad type"):
        console_failing_function()
    captured = capsys.readouterr()
    # Проверяем, что сообщение об ошибке было напечатано в stdout
    # (Ваша функция _write_log пишет ошибки в stdout, а не stderr)
    assert "console_failing_function error: TypeError." in captured.out
    assert "(duration:" in captured.out