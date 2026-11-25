from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class Submission:
    student_id: str
    laboratory_id: str
    attempt: int
    score: float
    comment: str = ""

    def __post_init__(self) -> None:
        """Проверяет инварианты попытки сдачи."""
        if not isinstance(self.student_id, str) or not self.student_id.strip():
            raise ValueError("student_id не должен быть пустым")
        if not isinstance(self.laboratory_id, str) or not self.laboratory_id.strip():
            raise ValueError("laboratory_id не должен быть пустым")
        if (
            not isinstance(self.attempt, int)
            or isinstance(self.attempt, bool)
            or self.attempt <= 0
        ):
            raise ValueError("attempt должен быть положительным целым числом")
        if isinstance(self.score, bool) or not isinstance(self.score, (int, float)):
            raise ValueError("score должен быть числом")
        if not 0 <= self.score <= 100:
            raise ValueError("score должен находиться в диапазоне от 0 до 100")
        if not isinstance(self.comment, str):
            raise ValueError("comment должен быть строкой")

    @property
    def sort_key(self) -> tuple[int, float]:
        """Ключ сортировки работ: сначала номер попытки, затем результат."""
        return self.attempt, self.score


class Student:
    """Студент и его попытки сдачи лабораторных работ."""

    def __init__(self, student_id: str, full_name: str) -> None:
        if not self.is_valid_id(student_id):
            raise ValueError("student_id должен быть непустой строкой")
        if not isinstance(full_name, str) or not full_name.strip():
            raise ValueError("full_name должен быть непустой строкой")

        self._student_id = student_id.strip()
        self._full_name = " ".join(full_name.split())
        self._submissions: list[Submission] = []

    @classmethod
    def from_full_name(cls, student_id: str, full_name: str) -> Student:
        """Альтернативный конструктор: нормализует полное имя студента."""
        if not isinstance(full_name, str):
            raise ValueError("full_name должен быть строкой")
        parts = full_name.split()
        if not parts:
            raise ValueError("full_name не должен быть пустым")

        normalized = " ".join(part[:1].upper() + part[1:].lower() for part in parts)
        return cls(student_id, normalized)

    @staticmethod
    def is_valid_id(student_id: object) -> bool:
        """Проверяет корректность идентификатора студента."""
        return isinstance(student_id, str) and bool(student_id.strip())

    @property
    def student_id(self) -> str:
        """Идентификатор студента."""
        return self._student_id

    @property
    def full_name(self) -> str:
        """Полное имя студента."""
        return self._full_name

    @property
    def submissions(self) -> tuple[Submission, ...]:
        """Неизменяемое представление списка работ студента."""
        return tuple(self._submissions)

    @property
    def average_score(self) -> float:
        """Средний результат по всем попыткам (0.0, если попыток нет)."""
        if not self._submissions:
            return 0.0
        return sum(submission.score for submission in self._submissions) / len(
            self._submissions
        )

    def add_submission(self, submission: Submission) -> None:
        if not isinstance(submission, Submission):
            raise TypeError("submission должен быть объектом Submission")
        if submission.student_id != self._student_id:
            raise ValueError("Работа принадлежит другому студенту")

        self._submissions.append(submission)

    def best_score(self, laboratory_id: str) -> float | None:
        """Возвращает лучший результат по работе или ``None``."""
        scores = [
            submission.score
            for submission in self._submissions
            if submission.laboratory_id == laboratory_id
        ]
        return max(scores) if scores else None

    def sorted_submissions(self) -> list[Submission]:
        return sorted(self._submissions, key=lambda submission: submission.sort_key)

    def __len__(self) -> int:
        """Количество попыток сдачи."""
        return len(self._submissions)

    def __iter__(self) -> Iterator[Submission]:
        """Обход попыток студента в порядке добавления."""
        return iter(self._submissions)

    def __str__(self) -> str:
        """Человекочитаемое представление студента."""
        return (
            f"Студент {self._student_id} «{self._full_name}»: "
            f"попыток {len(self)}, средний балл {self.average_score:.2f}"
        )

    def __repr__(self) -> str:
        """Однозначное отладочное представление студента."""
        return (
            f"Student(student_id={self._student_id!r}, "
            f"full_name={self._full_name!r}, submissions={self._submissions!r})"
        )


class Course:
    """Учебный курс: реестр студентов и приём их работ."""

    def __init__(self) -> None:
        """Создаёт пустой курс."""
        self._students: dict[str, Student] = {}

    def add_student(self, student: Student) -> None:
        if not isinstance(student, Student):
            raise TypeError("student должен быть объектом Student")
        if student.student_id in self._students:
            raise ValueError(
                f"Студент с идентификатором {student.student_id!r} уже зарегистрирован"
            )
        self._students[student.student_id] = student

    def get_student(self, student_id: str) -> Student:
        try:
            return self._students[student_id]
        except KeyError:
            raise KeyError(f"Студент {student_id!r} не зарегистрирован") from None

    def submit(
        self,
        student_id: str,
        laboratory_id: str,
        attempt: int,
        score: float,
        comment: str = "",
    ) -> Submission:
        """Создаёт и добавляет попытку сдачи работы."""
        student = self.get_student(student_id)
        submission = Submission(
            student_id=student_id,
            laboratory_id=laboratory_id,
            attempt=attempt,
            score=score,
            comment=comment,
        )
        student.add_submission(submission)
        return submission

    def top_students(self, limit: int = 3) -> list[Student]:
        if limit <= 0:
            return []
        return sorted(
            self._students.values(),
            key=lambda student: (-student.average_score, student.student_id),
        )[:limit]

    def __contains__(self, student_id: object) -> bool:
        """Проверяет, зарегистрирован ли студент с таким идентификатором."""
        return isinstance(student_id, str) and student_id in self._students

    def __len__(self) -> int:
        """Количество зарегистрированных студентов."""
        return len(self._students)

    def __iter__(self) -> Iterator[Student]:
        """Обход студентов в порядке регистрации."""
        return iter(self._students.values())

    def __repr__(self) -> str:
        """Отладочное представление курса."""
        return f"Course(students={len(self)})"


def _print_section(title: str) -> None:
    """Печатает заголовок демонстрационного раздела."""
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


if __name__ == "__main__":
    course = Course()

    ivan = Student.from_full_name("S-001", "  иВАН   петров ")
    anna = Student.from_full_name("S-002", "анна смирнова")
    boris = Student.from_full_name("S-003", "борис кузнецов")
    for student in (ivan, anna, boris):
        course.add_student(student)

    _print_section("1. Созданные студенты")
    for student in course:
        print(student)

    _print_section("2. Добавление попыток сдачи")
    course.submit("S-001", "lab_02", 1, 88.0)
    course.submit("S-001", "lab_01", 1, 72.0, "Есть замечания по оформлению")
    course.submit("S-001", "lab_01", 2, 91.0, "Замечания исправлены")
    course.submit("S-002", "lab_01", 1, 95.0, "Отличная работа")
    course.submit("S-002", "lab_02", 1, 89.0)
    course.submit("S-003", "lab_01", 1, 64.0)

    for student in course:
        print(student)

    _print_section("3. Стандартные функции len(), iter() и оператор in")
    print("len(course):", len(course))
    print("iter(course):", ", ".join(student.full_name for student in course))
    print("'S-002' in course:", "S-002" in course)
    print("'S-999' in course:", "S-999" in course)

    ivan = course.get_student("S-001")
    print("len(ivan):", len(ivan))
    print("iter(ivan):", list(ivan))
    print("ivan.average_score:", f"{ivan.average_score:.2f}")
    print("ivan.best_score('lab_01'):", ivan.best_score("lab_01"))
    print("ivan.best_score('lab_99'):", ivan.best_score("lab_99"))

    _print_section("4. Свойство submissions защищает внутренний список")
    print("тип submissions:", type(ivan.submissions).__name__)
    try:
        ivan.submissions.append(
            Submission("S-001", "lab_03", 1, 100.0)
        )
    except AttributeError as error:
        print("изменить снаружи нельзя:", error)

    _print_section("5. Сортировка без изменения внутреннего порядка")
    print("порядок добавления:")
    for submission in ivan:
        print(
            f"  {submission.laboratory_id}, попытка {submission.attempt}, "
            f"{submission.score}"
        )

    print("отсортированное представление:")
    for submission in ivan.sorted_submissions():
        print(
            f"  {submission.laboratory_id}, попытка {submission.attempt}, "
            f"{submission.score}"
        )

    print("внутренний порядок после сортировки:")
    print("  ", [(item.attempt, item.laboratory_id) for item in ivan])

    _print_section("6. Сравнение Submission по содержимому")
    first = Submission("S-001", "lab_03", 1, 80.0, "ок")
    second = Submission("S-001", "lab_03", 1, 80.0, "ок")
    third = Submission("S-001", "lab_03", 1, 81.0, "ок")
    print("first == second:", first == second)
    print("first is second:", first is second)
    print("first == third:", first == third)
    print("hash(first) == hash(second):", hash(first) == hash(second))

    _print_section("7. Проверка инвариантов Submission")
    invalid_cases = (
        ("", "lab_01", 1, 80.0),
        ("S-001", "", 1, 80.0),
        ("S-001", "lab_01", 0, 80.0),
        ("S-001", "lab_01", 1, 101.0),
        ("S-001", "lab_01", 1, -1.0),
    )
    for arguments in invalid_cases:
        try:
            Submission(*arguments)
        except ValueError as error:
            print("ValueError:", error)

    _print_section("8. Статическая проверка id и топ студентов")
    print("Student.is_valid_id('S-010'):", Student.is_valid_id("S-010"))
    print("Student.is_valid_id('   '):  ", Student.is_valid_id("   "))
    print("Student.is_valid_id(10):      ", Student.is_valid_id(10))

    for place, student in enumerate(course.top_students(), start=1):
        print(
            f"{place}. {student.full_name} — "
            f"{student.average_score:.2f} ({student.student_id})"
        )

    _print_section("9. repr() и str()")
    print("repr(ivan):", repr(ivan))
    print("str(ivan): ", ivan)
    print("repr(course):", repr(course))
