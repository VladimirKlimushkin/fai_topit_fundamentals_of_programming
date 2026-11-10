from typing import Optional


course = "Python-разработчик"


def arithmetic_mean(values: list[float]) -> float:
    """Возвращает среднее арифметическое непустого списка."""
    assert isinstance(values, list), "values должен быть списком"
    assert len(values) > 0, "values не должен быть пустым"
    assert all(isinstance(v, (int, float)) for v in values), "все элементы должны быть числами"

    if not values:
        raise ValueError("values не должен быть пустым")

    result = sum(values) / len(values)

    assert isinstance(result, float), "результат должен быть float"
    assert result == result, "результат не должен быть NaN"
    return result

def normalize_name(name: str) -> str:
    """Удаляет лишние пробелы и приводит каждую часть имени к нужному регистру."""
    assert isinstance(name, str), "name должен быть строкой"

    parts = name.split()
    if not parts:
        raise ValueError("name не должен быть пустым или состоять из пробелов")

    result = " ".join(part.capitalize() for part in parts)

    assert result == result.strip(), "в результате не должно быть пробелов по краям"
    assert "  " not in result, "в результате не должно быть двойных пробелов"
    return result

def build_report(
    student: str,
    results: list[int],
    *,
    precision: int = 2,
    prefix: str = "Результат",
) -> str:
    """Формирует строковый отчет о результатах студента."""
    assert isinstance(student, str), "student должен быть строкой"
    assert isinstance(results, list), "results должен быть списком"
    assert isinstance(precision, int) and precision >= 0, "precision — неотрицательный int"
    assert isinstance(prefix, str), "prefix должен быть строкой"

    if not results:
        raise ValueError("results не должен быть пустым")

    name = normalize_name(student)
    avg = arithmetic_mean(results)
    report = f"{prefix} для {name}: {avg:.{precision}f} (оценок: {len(results)})"

    assert isinstance(report, str), "отчёт должен быть строкой"
    assert name in report, "имя должно присутствовать в отчёте"
    assert str(len(results)) in report, "количество оценок должно быть в отчёте"
    return report


def collect_tags(*tags: str, lowercase: bool = True) -> tuple[str, ...]:
    """Возвращает очищенные теги без пустых значений и повторов."""
    assert all(isinstance(t, str) for t in tags), "все теги должны быть строками"
    assert isinstance(lowercase, bool), "lowercase должен быть bool"

    seen: set[str] = set()
    result: list[str] = []
    for tag in tags:
        clean = tag.strip()
        if lowercase:
            clean = clean.lower()
        if not clean or clean in seen:
            continue
        seen.add(clean)
        result.append(clean)

    out = tuple(result)

    assert isinstance(out, tuple), "результат должен быть кортежем"
    assert all(t == t.strip() for t in out), "в тегах не должно быть пробелов по краям"
    assert len(out) == len(set(out)), "теги не должны повторяться"
    if lowercase:
        assert all(t == t.lower() for t in out), "при lowercase=True все теги в нижнем регистре"
    return out


def make_greeting(base: str = "Привет") -> str:
    """Внешняя функция: создаёт локальное имя 'who' в объемлющей области."""
    who = "студент"

    def inner(new_who: str) -> str:
        nonlocal who
        assert isinstance(new_who, str) and new_who.strip(), "new_who должен быть непустой строкой"
        who = new_who.strip()
        assert who == new_who.strip(), "who обновлён корректно"
        return f"{base}, {who}!"

    result = inner("Иван")
    assert who == "Иван", "nonlocal изменил объемлющую переменную"
    assert course == "Python-разработчик", "глобальное имя не тронуто"
    return result


def add_result(value, results: Optional[list] = None) -> list:
    """Возвращает НОВЫЙ список с добавленным value; входной список не мутируется."""
    assert isinstance(value, (int, float)), "value должно быть числом"
    assert results is None or isinstance(results, list), "results — список или None"

    if results is None:
        results = []
    out = [*results, value]

    assert out[-1] == value, "новое значение в конце"
    assert len(out) == len(results) + 1, "длина выросла на 1"
    assert results == (results if results is not None else []), "входной список не изменён"
    return out


def apply_to_results(operation, values):
    """Применяет operation к каждому элементу values, возвращает список."""
    assert callable(operation), "operation должна быть вызываемой"
    assert values is not None, "values не должен быть None"

    result = [operation(v) for v in values]

    assert isinstance(result, list), "результат — список"
    assert len(result) == len(values), "длина сохранена"
    return result


def double(x: float) -> float:
    return x * 2


def make_threshold_checker(threshold: float):
    """Возвращает функцию check(value) -> bool: прошёл ли результат порог."""
    assert isinstance(threshold, (int, float)), "threshold должно быть числом"

    def check(value: float) -> bool:
        assert isinstance(value, (int, float)), "value должно быть числом"
        return value >= threshold

    return check


if __name__ == "__main__":
    print(make_greeting())
    print(course)
    print("-----------------")
    print(add_result(1))
    print(add_result(2))
    print(add_result.__defaults__)
    print("-----------------")
    print(arithmetic_mean([1, 2, 3]))
    print(normalize_name("  иВАН   петров  "))
    print(build_report("  иВАН   петров  ", [4, 5, 3]))
    print(build_report("анна", [5, 5], precision=1))
    print(build_report("анна", [5, 5], prefix="Итог", precision=0))
    print(collect_tags("Python", " python ", "ML", ""))
    print(collect_tags("Python", "python", lowercase=False))
    print("-----------------")
    scores = [5, 4, 3]
    opts = {"precision": 1, "prefix": "Оценка"}
    print(build_report("иван", scores, **opts))
    tag_list = ["Python", " python ", "ML"]
    print(collect_tags(*tag_list))
    print("-----------------")
    print(apply_to_results(double, [1, 2, 3]))
    print(apply_to_results(lambda x: x ** 2, [1, 2, 3]))
    print(apply_to_results(lambda x: x + 10, [1, 2, 3]))
    print("-----------------")
    pass_60 = make_threshold_checker(60)
    pass_90 = make_threshold_checker(90)
    print(pass_60(75))
    print(pass_60(50))
    print(pass_90(75))
    print(pass_90(95))
    print(pass_60.__closure__[0].cell_contents)
    print(pass_90.__closure__[0].cell_contents)
    print(pass_60.__closure__ is pass_90.__closure__)
    print("-----------------")
    values = [55, 72, 88, 91, 40]
    check = make_threshold_checker(70)
    print(apply_to_results(check, values))
    print([v for v in values if check(v)])
