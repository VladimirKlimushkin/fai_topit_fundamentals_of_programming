students = {
    "Анна": [78, 91, 84, 88],
    "Борис": [60, 72, 68],
    "Дарья": [95, 93, 97, 90],
    "Илья": [55, 61],
}


def mean(values: list):
    return sum(values) / len(values)


def minimum(values: list):
    result = float("inf")
    for val in values:
        if val < result:
            result = val
    return result


def maximum(values: list):
    result = float("-inf")
    for val in values:
        if val > result:
            result = val
    return result


def classify(score: float) -> str:
    if score >= 90:
        return "отличный"
    if score >= 75:
        return "хороший"
    if score >= 60:
        return "удовлетворительный"
    return "недостаточный"


def student_summary(name: str, results: list[int]) -> dict:
    if not results:
        return {
            "name": name,
            "count": 0,
            "mean": None,
            "min": None,
            "max": None,
            "category": "нет результатов",
        }
    avg = mean(results)
    return {
        "name": name,
        "count": len(results),
        "mean": avg,
        "min": minimum(results),
        "max": maximum(results),
        "category": classify(avg),
    }


def group_summary(students: dict) -> dict:
    summaries = [student_summary(name, results) for name, results in students.items()]
    valid = [s for s in summaries if s["mean"] is not None]

    categories = {
        "отличный": 0,
        "хороший": 0,
        "удовлетворительный": 0,
        "недостаточный": 0,
        "нет результатов": 0,
    }
    for s in summaries:
        categories[s["category"]] += 1

    if valid:
        group_mean = sum(s["mean"] for s in valid) / len(valid)
        best = max(s["mean"] for s in valid)
        worst = min(s["mean"] for s in valid)
        leaders = [s["name"] for s in valid if s["mean"] == best]
    else:
        group_mean = None
        best = None
        worst = None
        leaders = []

    return {
        "students": summaries,
        "count": len(summaries),
        "categories": categories,
        "group_mean": group_mean,
        "best": best,
        "worst": worst,
        "leaders": leaders,
    }


def find_top_students(students: dict) -> list:
    valid = {
        name: mean(results)
        for name, results in students.items()
        if results
    }
    if not valid:
        return []
    top = maximum(list(valid.values()))
    return [name for name, avg in valid.items() if avg == top]


def format_report(student_data, group_data) -> str:
    lines = []
    lines.append("=" * 50)
    lines.append("ОТЧЁТ ПО РЕЗУЛЬТАТАМ ГРУППЫ")
    lines.append("=" * 50)

    for s in student_data:
        lines.append(f"\nСтудент: {s['name']}")
        lines.append(f"  Оценок: {s['count']}")
        if s["mean"] is None:
            lines.append("  Нет результатов")
            continue
        lines.append(f"  Средний: {s['mean']:.2f}")
        lines.append(f"  Минимум: {s['min']}")
        lines.append(f"  Максимум: {s['max']}")
        lines.append(f"  Категория: {s['category']}")

    lines.append("\n" + "-" * 50)
    lines.append("СВОДКА ПО ГРУППЕ")
    lines.append("-" * 50)
    lines.append(f"Всего студентов: {group_data['count']}")
    if group_data["group_mean"] is not None:
        lines.append(f"Средний балл группы: {group_data['group_mean']:.2f}")
        lines.append(f"Лучший средний: {group_data['best']:.2f}")
        lines.append(f"Худший средний: {group_data['worst']:.2f}")
    lines.append(f"Лидеры: {', '.join(group_data['leaders']) if group_data['leaders'] else 'нет'}")

    lines.append("\nРаспределение по категориям:")
    for cat, cnt in group_data["categories"].items():
        if cnt:
            lines.append(f"  {cat}: {cnt}")

    return "\n".join(lines)


def main():
    summaries = [student_summary(name, results) for name, results in students.items()]
    group_data = group_summary(students)
    print(format_report(summaries, group_data))
    print("\nТоп студентов:", find_top_students(students))


if __name__ == "__main__":
    main()
