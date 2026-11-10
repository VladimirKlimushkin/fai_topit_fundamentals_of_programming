submissions = [
    ("anna", "lab_01", 5),
    ("boris", "lab_01", 4),
    ("anna", "lab_02", 5),
    ("daria", "lab_01", 3),
    ("boris", "lab_02", 5),
    ("anna", "lab_01", 4),
]


def build_structures(submissions):
    students = set()
    labs = set()
    attempts_by_student = {}
    best_results = {}
    attempt_counts = {}

    for name, lab, score in submissions:
        students.add(name)
        labs.add(lab)

        attempts_by_student.setdefault(name, []).append((lab, score))

        key = (name, lab)
        if key not in best_results or score > best_results[key]:
            best_results[key] = score
        attempt_counts[key] = attempt_counts.get(key, 0) + 1

    return students, labs, attempts_by_student, best_results, attempt_counts


def add_submission(sub, structures):
    students, labs, attempts_by_student, best_results, attempt_counts = structures
    name, lab, score = sub

    students.add(name)
    labs.add(lab)
    attempts_by_student.setdefault(name, []).append((lab, score))

    key = (name, lab)
    if key not in best_results or score > best_results[key]:
        best_results[key] = score
    attempt_counts[key] = attempt_counts.get(key, 0) + 1


def students_both_labs(submissions, labs):
    labs = sorted(labs)
    if len(labs) < 2:
        return set()
    by_lab = {lab: set() for lab in labs}
    for name, lab, _ in submissions:
        by_lab[lab].add(name)
    result = set.intersection(*by_lab.values())
    return result


def process_query(line, structures, submissions):
    students, labs, attempts_by_student, best_results, attempt_counts = structures
    parts = line.strip().split()
    if not parts:
        return "Пустая команда."

    cmd = parts[0]

    match cmd:
        case "student":
            if len(parts) != 2:
                return "Использование: student <имя>"
            name = parts[1]
            if name not in students:
                return f"Студент '{name}' не найден."
            items = ", ".join(f"{lab}={score}" for lab, score in attempts_by_student[name])
            return f"Попытки {name}: {items}"

        case "best":
            if len(parts) != 3:
                return "Использование: best <имя> <lab>"
            key = (parts[1], parts[2])
            if key not in best_results:
                return f"Нет данных для {parts[1]} / {parts[2]}."
            return f"Лучший результат {parts[1]} по {parts[2]}: {best_results[key]}"

        case "attempts":
            if len(parts) != 3:
                return "Использование: attempts <имя> <lab>"
            key = (parts[1], parts[2])
            if key not in attempt_counts:
                return f"Нет данных для {parts[1]} / {parts[2]}."
            return f"Попыток {parts[1]} по {parts[2]}: {attempt_counts[key]}"

        case "completed":
            if len(parts) != 2:
                return "Использование: completed <lab>"
            lab = parts[1]
            if lab not in labs:
                return f"Работа '{lab}' не найдена."
            names = sorted({n for n, l, _ in submissions if l == lab})
            return f"Сдали {lab}: {', '.join(names)}"

        case _:
            return f"Неизвестная команда: {cmd}"


if __name__ == "__main__":
    structures = build_structures(submissions)
    students, labs, attempts_by_student, best_results, attempt_counts = structures

    print("=" * 60)
    print("Построенные структуры")
    print("=" * 60)
    print(f"Студенты:                 {sorted(students)}")
    print(f"Лабораторные работы:      {sorted(labs)}")
    print(f"Попытки по студентам:     {attempts_by_student}")
    print(f"Лучшие результаты:        {best_results}")
    print(f"Количество попыток:       {attempt_counts}")

    print()
    print(f"Сдавали обе работы: {sorted(students_both_labs(submissions, labs))}")

    print()
    print("=" * 60)
    print("Добавление записи ('daria', 'lab_02', 4)")
    print("=" * 60)
    add_submission(("daria", "lab_02", 4), structures)
    print(f"Студенты:                 {sorted(students)}")
    print(f"Лабораторные работы:      {sorted(labs)}")
    print(f"Лучшие результаты:        {best_results}")
    print(f"Количество попыток:       {attempt_counts}")

    print()
    print("=" * 60)
    print("Текстовые запросы (пустая строка — выход)")
    print("=" * 60)
    print("Доступно: student <имя> | best <имя> <lab> | attempts <имя> <lab> | completed <lab>")
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        if not line.strip():
            break
        print(process_query(line, structures, submissions))
