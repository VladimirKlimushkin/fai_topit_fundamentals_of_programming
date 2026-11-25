from __future__ import annotations

import gc
import tracemalloc
from collections import deque
from collections.abc import Callable, Iterable, Iterator
from typing import TypeVar

T = TypeVar("T")


def read_measurements(lines: Iterable[str]) -> Iterator[float]:
    for line in lines:
        text = line.strip()
        if not text:
            continue
        yield float(text)


def filter_range(
    values: Iterable[float], minimum: float, maximum: float
) -> Iterator[float]:
    """Пропускает только значения из закрытого диапазона [minimum, maximum]."""
    if minimum > maximum:
        raise ValueError("minimum не может быть больше maximum")

    for value in values:
        if minimum <= value <= maximum:
            yield value


def moving_average(values: Iterable[float], window_size: int) -> Iterator[float]:
    if not isinstance(window_size, int) or isinstance(window_size, bool):
        raise ValueError("window_size должен быть целым числом")
    if window_size <= 0:
        raise ValueError("window_size должен быть положительным")

    window: deque[float] = deque(maxlen=window_size)
    for value in values:
        window.append(value)
        if len(window) == window_size:
            yield sum(window) / window_size


def build_pipeline(
    lines: Iterable[str],
    minimum: float,
    maximum: float,
    window_size: int,
) -> Iterator[float]:
    """Собирает ленивый конвейер: строки → числа → фильтр → среднее."""
    numbers = read_measurements(lines)
    filtered = filter_range(numbers, minimum, maximum)
    return moving_average(filtered, window_size)


def take(n: int, iterable: Iterable[T]) -> Iterator[T]:
    if n < 0:
        raise ValueError("n не может быть отрицательным")

    iterator = iter(iterable)
    taken = 0
    while taken < n:
        try:
            value = next(iterator)
        except StopIteration:
            return
        yield value
        taken += 1


def drop(n: int, iterable: Iterable[T]) -> Iterator[T]:
    if n < 0:
        raise ValueError("n не может быть отрицательным")

    iterator = iter(iterable)
    dropped = 0
    while dropped < n:
        try:
            next(iterator)
        except StopIteration:
            return
        dropped += 1

    yield from iterator


def batch(iterable: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    if size <= 0:
        raise ValueError("size должен быть положительным")

    current: list[T] = []
    for value in iterable:
        current.append(value)
        if len(current) == size:
            yield tuple(current)
            current.clear()

    if current:
        yield tuple(current)


def eager_pipeline(
    lines: Iterable[str],
    minimum: float,
    maximum: float,
    window_size: int,
) -> list[float]:
    numbers = [float(line) for line in lines if line.strip()]
    filtered = [value for value in numbers if minimum <= value <= maximum]

    averages: list[float] = []
    window: deque[float] = deque(maxlen=window_size)
    for value in filtered:
        window.append(value)
        if len(window) == window_size:
            averages.append(sum(window) / window_size)

    return averages


def peak_memory(factory: Callable[[], Iterable[float]]) -> tuple[int, int]:
    """Измеряет пиковую память при полном обходе результата ``factory()``."""
    gc.collect()
    tracemalloc.start()
    result = factory()
    count = sum(1 for _ in result)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak, count


def _print_section(title: str) -> None:
    """Печатает заголовок демонстрационного раздела."""
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


if __name__ == "__main__":
    raw_lines = ["10.0", "", "12.5", "100.0", "11.5", "13.0", "9.5"]
    original_snapshot = raw_lines.copy()

    _print_section("1. Ленивый конвейер измерений")
    print("Исходные строки:", raw_lines)
    print("Диапазон фильтра: [9; 20], размер окна: 2")

    pipeline = build_pipeline(raw_lines, 9.0, 20.0, 2)
    first = next(pipeline)
    second = next(pipeline)
    rest = list(pipeline)
    print("первые два значения через next():", first, second)
    print("оставшиеся значения:", rest)

    print("исходный список не изменился:", raw_lines == original_snapshot)

    _print_section("2. Повторный обход исчерпанного и нового генератора")
    print("исчерпанный генератор:", list(pipeline))
    new_pipeline = build_pipeline(raw_lines, 9.0, 20.0, 2)
    print("новый конвейер:       ", list(new_pipeline))
    print("Генератор одноразовый, но новый вызов создаёт новый обход.")

    _print_section("3. Включения и генераторные выражения")
    squares_of_even = [number**2 for number in range(1, 21) if number % 2 == 0]
    nonempty_lengths = {
        len(line) for line in ["", "abc", "   ", "hello", "abc", "Python"] if line.strip()
    }
    squares_by_number = {number: number**2 for number in range(1, 11)}
    sum_of_squares = sum(number**2 for number in range(1_000_001))

    print("квадраты чётных чисел от 1 до 20:", squares_of_even)
    print("множество длин непустых строк:   ", sorted(nonempty_lengths))
    print("словарь число → квадрат:          ", squares_by_number)
    print("сумма квадратов от 1 до 1 000 000:", sum_of_squares)

    _print_section("4. take(), drop() и batch() вместе с конвейером")
    filtered = filter_range(read_measurements(raw_lines), 9.0, 20.0)
    print("take(3):   ", list(take(3, filtered)))

    filtered = filter_range(read_measurements(raw_lines), 9.0, 20.0)
    print("drop(2):   ", list(drop(2, filtered)))

    batches = batch(build_pipeline(raw_lines, 9.0, 20.0, 2), 2)
    print("batch(..., 2):", list(batches))

    _print_section("5. Некорректный размер окна")
    try:
        next(moving_average([1.0, 2.0, 3.0], 0))
    except ValueError as error:
        print("ValueError:", error)

    _print_section("6. Сравнение памяти: ленивый и жадный конвейеры")
    large_lines = [str(index % 90 + 10) for index in range(100_000)]

    lazy_peak, lazy_count = peak_memory(
        lambda: build_pipeline(large_lines, 0.0, 100.0, 5)
    )
    eager_peak, eager_count = peak_memory(
        lambda: eager_pipeline(large_lines, 0.0, 100.0, 5)
    )

    print(f"ленивый конвейер: {lazy_peak / 1024:.1f} КиБ, значений: {lazy_count}")
    print(f"жадный конвейер:  {eager_peak / 1024:.1f} КиБ, значений: {eager_count}")
    print(f"отношение пиковой памяти: {eager_peak / lazy_peak:.1f}×")
