from __future__ import annotations

from collections.abc import Iterator


class StepRange:

    __slots__ = ("_start", "_stop", "_step")

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        for name, value in (("start", start), ("stop", stop), ("step", step)):
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"{name} должен быть целым числом")

        if step == 0:
            raise ValueError("Шаг step не может быть равен нулю")

        self._start = start
        self._stop = stop
        self._step = step

    @property
    def start(self) -> int:
        """Начальное значение диапазона."""
        return self._start

    @property
    def stop(self) -> int:
        """Граница, которая не включается в диапазон."""
        return self._stop

    @property
    def step(self) -> int:
        """Шаг последовательности."""
        return self._step

    def __iter__(self) -> StepRangeIterator:
        """Создаёт новый независимый итератор для текущего диапазона."""
        return StepRangeIterator(self)

    def __len__(self) -> int:
        """Возвращает количество элементов без их перебора."""
        if self._step > 0:
            if self._start >= self._stop:
                return 0
            return (self._stop - self._start + self._step - 1) // self._step

        if self._start <= self._stop:
            return 0
        return (self._stop - self._start + self._step + 1) // self._step

    def __contains__(self, value: object) -> bool:
        if not isinstance(value, int):
            return False

        if self._step > 0:
            if not (self._start <= value < self._stop):
                return False
        else:
            if not (self._stop < value <= self._start):
                return False

        return (value - self._start) % self._step == 0

    def contains_by_scan(self, value: int) -> tuple[bool, int]:
        checked = 0
        iterator = iter(self)
        while True:
            try:
                current = next(iterator)
            except StopIteration:
                return False, checked
            checked += 1
            if current == value:
                return True, checked

    def __str__(self) -> str:
        return f"StepRange({self._start}, {self._stop}, {self._step})"

    def __repr__(self) -> str:
        return (
            f"StepRange(start={self._start!r}, stop={self._stop!r}, "
            f"step={self._step!r})"
        )


class StepRangeIterator:
    __slots__ = ("_step_range", "_current")

    def __init__(self, step_range: StepRange) -> None:
        """Создаёт итератор, установленный в начало диапазона."""
        self._step_range = step_range
        self._current = step_range.start

    @property
    def current(self) -> int:
        """Значение, которое будет возвращено следующим вызовом ``next()``."""
        return self._current

    def __iter__(self) -> StepRangeIterator:
        """Итератор возвращает самого себя."""
        return self

    def __next__(self) -> int:
        """Возвращает очередное значение или возбуждает ``StopIteration``."""
        step_range = self._step_range

        if step_range.step > 0:
            if self._current >= step_range.stop:
                raise StopIteration
        else:
            if self._current <= step_range.stop:
                raise StopIteration

        value = self._current
        self._current += step_range.step
        return value


def _print_section(title: str) -> None:
    """Печатает заголовок демонстрационного раздела."""
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


if __name__ == "__main__":
    _print_section("1. Базовые случаи StepRange")
    cases = (
        StepRange(0, 5, 1),
        StepRange(5, 0, -1),
        StepRange(0, 0, 1),
        StepRange(0, 5, -1),
        StepRange(2, 11, 3),
    )
    for step_range in cases:
        print(f"{step_range!s:<28} -> {list(step_range)}")

    _print_section("2. Нулевой шаг отклоняется")
    try:
        StepRange(0, 5, 0)
    except ValueError as error:
        print("ValueError:", error)

    _print_section("3. Повторный обход")
    numbers = StepRange(2, 11, 3)
    print("первый обход: ", list(numbers))
    print("второй обход: ", list(numbers))

    _print_section("4. Два независимых итератора одного диапазона")
    step_range = StepRange(0, 6, 2)
    first = iter(step_range)
    second = iter(step_range)
    print(f"исходно: first.current={first.current}, second.current={second.current}")

    for name, iterator in (
        ("first ", first),
        ("second", second),
        ("first ", first),
        ("second", second),
        ("first ", first),
        ("second", second),
    ):
        try:
            value = next(iterator)
            print(
                f"{name} -> {value:<2}; "
                f"first.current={first.current}, second.current={second.current}"
            )
        except StopIteration:
            print(
                f"{name} -> StopIteration; "
                f"first.current={first.current}, second.current={second.current}"
            )

    for name, iterator in (("first ", first), ("second", second)):
        try:
            next(iterator)
        except StopIteration:
            print(f"{name} после исчерпания -> StopIteration")

    _print_section("5. len(), in, __repr__")
    print("len(StepRange(2, 11, 3)):  ", len(StepRange(2, 11, 3)))
    print("len(StepRange(11, 2, -3)): ", len(StepRange(11, 2, -3)))
    print("5 in StepRange(2, 11, 3):  ", 5 in StepRange(2, 11, 3))
    print("6 in StepRange(2, 11, 3):  ", 6 in StepRange(2, 11, 3))
    print("100 in StepRange(0, 10, 1):", 100 in StepRange(0, 10, 1))
    print("repr:", repr(StepRange(2, 11, 3)))

    _print_section("6. Сравнение __contains__ с последовательным перебором")
    big_range = StepRange(0, 1_000_000, 1)
    target = 999_999

    print("Проверка через __contains__:", target in big_range)
    found, checked = big_range.contains_by_scan(target)
    print("Проверка последовательным перебором:", found)
    print("Проверено элементов при переборе:", checked)
    print("__contains__ выполняет фиксированное число операций (O(1)).")
