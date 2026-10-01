import pytest

from src.decorators import log


def test_log_success_console(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(2, 3)

    captured = capsys.readouterr()

    assert result == 5
    assert "add" in captured.out
    assert "5" in captured.out


def test_log_error_console(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()

    assert "divide" in captured.out
    assert "ZeroDivisionError" in captured.out
    assert "10" in captured.out
    assert "0" in captured.out


def test_log_success_file(tmp_path) -> None:
    log_file = tmp_path / "test.log"

    @log(str(log_file))
    def multiply(a: int, b: int) -> int:
        return a * b

    result = multiply(4, 5)

    content = log_file.read_text(encoding="utf-8")

    assert result == 20
    assert "multiply" in content
    assert "20" in content


def test_log_error_file(tmp_path) -> None:
    log_file = tmp_path / "test.log"

    @log(str(log_file))
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    content = log_file.read_text(encoding="utf-8")

    assert "divide" in content
    assert "ZeroDivisionError" in content
    assert "10" in content
    assert "0" in content
