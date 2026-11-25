from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any

from task_2 import StepRange


def consume(iterable: Iterable[Any]) -> list[Any]:
    result: list[Any] = []
    iterator = iter(iterable)
    while True:
        try:
            result.append(next(iterator))
        except StopIteration:
            return result


def my_enumerate(iterable: Iterable[Any], start: int = 0) -> Iterator[tuple[int, Any]]:
    iterator = iter(iterable)
    index = start
    while True:
        try:
            value = next(iterator)
        except StopIteration:
            return
        yield index, value
        index += 1


def my_zip(first: Iterable[Any], second: Iterable[Any]) -> Iterator[tuple[Any, Any]]:
    """Упрощённый аналог ``zip()`` для двух источников.

    Обход завершается, как только исчерпан самый короткий источник.
    Функция работает с любыми итерируемыми объектами, а не только
    со списками.
    """
    first_iterator = iter(first)
    second_iterator = iter(second)
    while True:
        try:
            first_value = next(first_iterator)
            second_value = next(second_iterator)
        except StopIteration:
            return
        yield first_value, second_value


def _print_section(title: str) -> None:
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


if __name__ == "__main__":
    _print_section("1. Исследование протокола итерации")
    values = [10, 20, 30]
    iterator = iter(values)

    print("iterator is values:", iterator is values)
    print("iter(iterator) is iterator:", iter(iterator) is iterator)
    print("next(iterator):", next(iterator))
    print("next(iterator):", next(iterator))
    print("next(iterator):", next(iterator))

    try:
        next(iterator)
    except StopIteration:
        print("четвёртый next(iterator): StopIteration")

    _print_section("2. Проверка consume()")
    print("список:              ", consume([1, 2, 3]))
    print("кортеж:              ", consume((4, 5, 6)))
    print("строка:              ", consume("abc"))
    print("range:               ", consume(range(3)))

    partially_used = iter([10, 20, 30, 40])
    print("первый элемент частично использованного итератора:", next(partially_used))
    print("остаток того же итератора:                        ", consume(partially_used))

    _print_section("3. Повторный обход списка и его итератора")
    repeatable = [1, 2, 3]
    one_shot = iter(repeatable)

    print("повторный consume(список):   ", consume(repeatable), consume(repeatable))
    print("повторный consume(итератор): ", consume(one_shot), consume(one_shot))
    print("Итератор одноразовый: после исчерпания он остаётся пустым.")

    _print_section("4. my_enumerate()")
    print("список:          ", list(my_enumerate(["a", "b", "c"])))
    print("строка, start=5: ", list(my_enumerate("xyz", start=5)))
    print("генератор:       ", list(my_enumerate(i * i for i in range(4))))
    print("StepRange:       ", list(my_enumerate(StepRange(2, 11, 3), start=1)))

    _print_section("5. my_zip()")
    print("список + строка:          ", list(my_zip([1, 2, 3], "ab")))
    print("строка + кортеж:          ", list(my_zip("abc", (10, 20))))
    print("генератор + range:        ", list(my_zip((x for x in range(5)), range(3))))
    print("StepRange + строка:       ", list(my_zip(StepRange(0, 6, 2), "abcd")))
