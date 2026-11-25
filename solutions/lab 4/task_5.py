"""Лабораторная работа № 4, задание 5. Расширяемый журнал курса.

Иерархия событий построена на абстрактном базовом классе ``CourseEvent``.
Журнал использует композицию, поддерживает протоколы ``len()``, ``iter()``,
индексацию и срезы, а также предоставляет ленивые представления событий.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import Counter
from collections.abc import Callable, Iterable, Iterator
from datetime import datetime, timedelta
from pprint import pprint

from task_4 import Course, Student, Submission


class CourseEvent(ABC):
    """Абстрактное событие учебного курса."""

    def __init__(self, student_id: str, *, created_at: datetime | None = None) -> None:
        """Сохраняет идентификатор студента и время создания события."""
        if not isinstance(student_id, str) or not student_id.strip():
            raise ValueError("student_id не должен быть пустым")
        if created_at is not None and not isinstance(created_at, datetime):
            raise TypeError("created_at должен быть datetime")

        self._student_id = student_id
        self._created_at = created_at if created_at is not None else datetime.now()

    @property
    @abstractmethod
    def student_id(self) -> str:
        """Идентификатор студента, к которому относится событие."""

    @property
    def created_at(self) -> datetime:
        """Время создания события."""
        return self._created_at

    @abstractmethod
    def describe(self) -> str:
        """Возвращает человекочитаемое описание события."""

    def __str__(self) -> str:
        """Строковое представление совпадает с описанием события."""
        return self.describe()

    def __repr__(self) -> str:
        """Отладочное представление общего вида."""
        return (
            f"{type(self).__name__}(student_id={self.student_id!r}, "
            f"created_at={self.created_at.isoformat()!r})"
        )


class SubmissionEvent(CourseEvent):
    """Событие сдачи лабораторной работы."""

    def __init__(self, submission: Submission, *, created_at: datetime | None = None) -> None:
        """Создаёт событие на основе объекта ``Submission``."""
        if not isinstance(submission, Submission):
            raise TypeError("submission должен быть объектом Submission")
        super().__init__(submission.student_id, created_at=created_at)
        self._submission = submission

    @property
    def student_id(self) -> str:
        """Идентификатор студента."""
        return self._submission.student_id

    @property
    def submission(self) -> Submission:
        """Исходная попытка сдачи."""
        return self._submission

    @property
    def laboratory_id(self) -> str:
        """Идентификатор лабораторной работы."""
        return self._submission.laboratory_id

    @property
    def attempt(self) -> int:
        """Номер попытки."""
        return self._submission.attempt

    @property
    def score(self) -> float:
        """Результат попытки."""
        return self._submission.score

    @property
    def comment(self) -> str:
        """Комментарий к попытке."""
        return self._submission.comment

    def describe(self) -> str:
        """Описывает сдачу работы."""
        description = (
            f"{self.student_id}: сдача {self.laboratory_id}, "
            f"попытка {self.attempt}, результат {self.score:g}"
        )
        if self.comment:
            description += f" ({self.comment})"
        return description


class AttendanceEvent(CourseEvent):
    """Событие посещения занятия."""

    def __init__(
        self,
        student_id: str,
        lesson: str,
        *,
        present: bool = True,
        created_at: datetime | None = None,
    ) -> None:
        """Создаёт событие посещения или пропуска занятия."""
        super().__init__(student_id, created_at=created_at)
        if not isinstance(lesson, str) or not lesson.strip():
            raise ValueError("lesson не должен быть пустым")
        if not isinstance(present, bool):
            raise TypeError("present должен быть bool")

        self._lesson = lesson.strip()
        self._present = present

    @property
    def student_id(self) -> str:
        """Идентификатор студента."""
        return self._student_id

    @property
    def lesson(self) -> str:
        """Название занятия."""
        return self._lesson

    @property
    def present(self) -> bool:
        """Признак присутствия студента."""
        return self._present

    def describe(self) -> str:
        """Описывает посещение или пропуск."""
        action = "посетил(а)" if self._present else "пропустил(а)"
        return f"{self.student_id}: {action} занятие «{self._lesson}»"


class CommentEvent(CourseEvent):
    """Событие текстовой обратной связи."""

    def __init__(
        self, student_id: str, text: str, *, created_at: datetime | None = None
    ) -> None:
        """Создаёт событие с текстовым комментарием."""
        super().__init__(student_id, created_at=created_at)
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text не должен быть пустым")

        self._text = text.strip()

    @property
    def student_id(self) -> str:
        """Идентификатор студента."""
        return self._student_id

    @property
    def text(self) -> str:
        """Текст комментария."""
        return self._text

    def describe(self) -> str:
        """Описывает комментарий."""
        return f"{self.student_id}: комментарий «{self._text}»"


class DeadlineEvent(CourseEvent):
    """Событие срока сдачи лабораторной работы."""

    def __init__(
        self,
        student_id: str,
        laboratory_id: str,
        deadline: datetime,
        *,
        created_at: datetime | None = None,
    ) -> None:
        """Создаёт событие дедлайна."""
        super().__init__(student_id, created_at=created_at)
        if not isinstance(laboratory_id, str) or not laboratory_id.strip():
            raise ValueError("laboratory_id не должен быть пустым")
        if not isinstance(deadline, datetime):
            raise TypeError("deadline должен быть datetime")

        self._laboratory_id = laboratory_id
        self._deadline = deadline

    @property
    def student_id(self) -> str:
        """Идентификатор студента."""
        return self._student_id

    @property
    def laboratory_id(self) -> str:
        """Идентификатор лабораторной работы."""
        return self._laboratory_id

    @property
    def deadline(self) -> datetime:
        """Момент окончания срока сдачи."""
        return self._deadline

    def describe(self) -> str:
        """Описывает дедлайн."""
        return (
            f"{self.student_id}: срок сдачи {self._laboratory_id} — "
            f"{self._deadline:%d.%m.%Y %H:%M}"
        )


class CourseJournal:
    """Журнал событий курса в порядке добавления."""

    def __init__(self, events: Iterable[CourseEvent] | None = None) -> None:
        """Создаёт журнал, при необходимости заполняя его событиями."""
        self._events: list[CourseEvent] = []
        if events is not None:
            for event in events:
                self.add_event(event)

    def add_event(self, event: CourseEvent) -> None:
        """Добавляет событие в конец журнала.

        Raises:
            TypeError: если передан объект не ``CourseEvent``.
        """
        if not isinstance(event, CourseEvent):
            raise TypeError("event должен быть объектом CourseEvent")
        self._events.append(event)

    def events_for_student(self, student_id: str) -> Iterator[CourseEvent]:
        """Лениво перебирает события указанного студента."""
        for event in self._events:
            if event.student_id == student_id:
                yield event

    def events_by_type(self, event_type: type[CourseEvent]) -> Iterator[CourseEvent]:
        """Лениво перебирает события указанного типа.

        Проверка типа выполняется через ``isinstance``, поэтому для
        подкласса ``CourseEvent`` возвращаются и его наследники.
        """
        if not isinstance(event_type, type) or not issubclass(event_type, CourseEvent):
            raise TypeError("event_type должен быть подклассом CourseEvent")

        for event in self._events:
            if isinstance(event, event_type):
                yield event

    def summary(self) -> dict[str, object]:
        """Возвращает агрегированные данные без внутреннего списка событий."""
        by_type = Counter(type(event).__name__ for event in self._events)
        by_student = Counter(event.student_id for event in self._events)

        scores = [
            event.score
            for event in self._events
            if isinstance(event, SubmissionEvent)
        ]

        return {
            "total_events": len(self._events),
            "by_type": dict(by_type),
            "by_student": dict(by_student),
            "students": tuple(by_student),
            "submission_count": len(scores),
            "average_score": (sum(scores) / len(scores)) if scores else None,
        }

    def __len__(self) -> int:
        """Количество событий в журнале."""
        return len(self._events)

    def __iter__(self) -> Iterator[CourseEvent]:
        """Обход событий в порядке добавления."""
        return iter(self._events)

    def __getitem__(self, index: int | slice) -> CourseEvent | tuple[CourseEvent, ...]:
        """Возвращает событие по индексу или кортеж событий по срезу."""
        if isinstance(index, slice):
            return tuple(self._events[index])
        return self._events[index]

    def __str__(self) -> str:
        """Человекочитаемое представление журнала."""
        students_count = len({event.student_id for event in self._events})
        return f"Журнал курса: событий {len(self)}, студентов {students_count}"

    def __repr__(self) -> str:
        """Отладочное представление журнала."""
        return f"CourseJournal(events={len(self)})"


def render_timeline(events: Iterable[CourseEvent]) -> str:
    """Формирует временную шкалу, вызывая describe() у каждого события.

    Функция не проверяет конкретные типы событий: она опирается только
    на общий интерфейс ``created_at`` и ``describe()``.
    """
    lines = [
        f"{event.created_at:%d.%m.%Y %H:%M} — {event.describe()}" for event in events
    ]
    return "\n".join(lines) if lines else "Событий нет."


class ScoreView:
    """Ленивое итерируемое представление результатов сдач.

    При каждом обходе создаётся новый генератор, поэтому представление
    можно обходить повторно, если исходный объект повторно итерируем.
    """

    def __init__(self, events: Iterable[CourseEvent]) -> None:
        """Сохраняет источник событий."""
        self._events = events

    def __iter__(self) -> Iterator[float]:
        """Выдаёт результаты только событий сдачи."""
        for event in self._events:
            if isinstance(event, SubmissionEvent):
                yield event.score

    def __len__(self) -> int:
        """Количество результатов сдачи."""
        return sum(1 for _ in self)

    def average(self) -> float | None:
        """Средний результат сдачи или ``None``, если сдач нет."""
        total = 0.0
        count = 0
        for score in self:
            total += score
            count += 1
        return total / count if count else None

    def best(self) -> float | None:
        """Лучший результат сдачи или ``None``, если сдач нет."""
        best_score: float | None = None
        for score in self:
            if best_score is None or score > best_score:
                best_score = score
        return best_score

    def __repr__(self) -> str:
        """Отладочное представление представления результатов."""
        return "ScoreView()"


class FilteredJournalView:
    """Ленивое представление журнала, отбирающее события предикатом."""

    def __init__(
        self, journal: CourseJournal, predicate: Callable[[CourseEvent], bool]
    ) -> None:
        """Сохраняет журнал и функцию-предикат."""
        if not isinstance(journal, CourseJournal):
            raise TypeError("journal должен быть объектом CourseJournal")
        if not callable(predicate):
            raise TypeError("predicate должен быть вызываемым объектом")

        self._journal = journal
        self._predicate = predicate

    def __iter__(self) -> Iterator[CourseEvent]:
        """Лениво выдаёт события, для которых предикат истинен."""
        for event in self._journal:
            if self._predicate(event):
                yield event

    def __len__(self) -> int:
        """Количество подходящих событий."""
        return sum(1 for _ in self)

    def __repr__(self) -> str:
        """Отладочное представление отфильтрованного журнала."""
        return f"FilteredJournalView(events={len(self)})"


def _print_section(title: str) -> None:
    """Печатает заголовок демонстрационного раздела."""
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


if __name__ == "__main__":
    course = Course()
    students = (
        Student.from_full_name("S-001", "иван петров"),
        Student.from_full_name("S-002", "анна смирнова"),
        Student.from_full_name("S-003", "борис кузнецов"),
    )
    for student in students:
        course.add_student(student)

    base_time = datetime(2026, 11, 20, 9, 0)

    def at(minutes: int) -> datetime:
        """Возвращает время через указанное число минут после начала дня."""
        return base_time + timedelta(minutes=minutes)

    first_attempt = course.submit(
        "S-001", "lab_01", 1, 72.0, "Есть замечания по оформлению"
    )
    second_attempt = course.submit(
        "S-001", "lab_01", 2, 91.0, "Замечания исправлены"
    )
    anna_first = course.submit("S-002", "lab_01", 1, 95.0, "Отличная работа")
    boris_first = course.submit("S-003", "lab_01", 1, 64.0)
    anna_second = course.submit("S-002", "lab_02", 1, 89.0)
    boris_second = course.submit("S-003", "lab_02", 1, 75.0)

    journal = CourseJournal(
        [
            SubmissionEvent(first_attempt, created_at=at(0)),
            AttendanceEvent(
                "S-001", "Итераторы и генераторы", present=True, created_at=at(15)
            ),
            CommentEvent(
                "S-001",
                "Разберитесь с ленивым выполнением генераторов",
                created_at=at(30),
            ),
            SubmissionEvent(anna_first, created_at=at(45)),
            SubmissionEvent(boris_first, created_at=at(55)),
            AttendanceEvent(
                "S-002", "Итераторы и генераторы", present=True, created_at=at(65)
            ),
            AttendanceEvent(
                "S-003", "Итераторы и генераторы", present=False, created_at=at(70)
            ),
            SubmissionEvent(second_attempt, created_at=at(85)),
            CommentEvent(
                "S-003", "Повторите протокол итерации", created_at=at(95)
            ),
            SubmissionEvent(anna_second, created_at=at(105)),
            SubmissionEvent(boris_second, created_at=at(120)),
        ]
    )

    _print_section("1. Журнал и протоколы len(), iter(), индексация")
    print("Студенты курса:", ", ".join(student.full_name for student in course))
    print("len(journal):", len(journal))
    print("journal[0]:", journal[0])
    print("journal[-1]:", journal[-1])
    print("срез journal[2:6]:")
    for event in journal[2:6]:
        print("  ", event)

    _print_section("2. Выборки по студенту и по типу события")
    print("События S-001:")
    for event in journal.events_for_student("S-001"):
        print("  ", event)

    print("События AttendanceEvent:")
    for event in journal.events_by_type(AttendanceEvent):
        print("  ", event)

    _print_section("3. Сводка по журналу")
    pprint(journal.summary())

    _print_section("4. Временная шкала до добавления DeadlineEvent")
    print(render_timeline(journal))

    _print_section("5. Статистика через ScoreView")
    score_view = ScoreView(journal)
    print("первый обход: ", list(score_view))
    print("второй обход: ", list(score_view))
    print("len(score_view):", len(score_view))
    print("средний результат:", f"{score_view.average():.2f}")
    print("лучший результат: ", score_view.best())

    _print_section("6. Расширение: DeadlineEvent без изменения render_timeline")
    deadline = DeadlineEvent(
        "S-003",
        "lab_02",
        datetime(2026, 12, 1, 23, 59),
        created_at=at(130),
    )
    journal.add_event(deadline)
    print("len(journal) после добавления:", len(journal))
    print("События DeadlineEvent:")
    for event in journal.events_by_type(DeadlineEvent):
        print("  ", event)
    print("render_timeline() без изменений:")
    print(render_timeline(journal))

    _print_section("7. FilteredJournalView: именованная функция")
    def is_s001(event: CourseEvent) -> bool:
        """Проверяет, что событие относится к студенту S-001."""
        return event.student_id == "S-001"

    s001_view = FilteredJournalView(journal, is_s001)
    print("первый обход:")
    for event in s001_view:
        print("  ", event)
    print("повторный обход:", [type(event).__name__ for event in s001_view])
    print("len(view):", len(s001_view))

    _print_section("8. FilteredJournalView: lambda")
    high_scores = FilteredJournalView(
        journal,
        lambda event: isinstance(event, SubmissionEvent) and event.score >= 85,
    )
    print("высокие результаты:")
    for event in high_scores:
        print("  ", event)
    print("повторный обход:", [type(event).__name__ for event in high_scores])

    _print_section("9. Итоговая сводка и repr()")
    pprint(journal.summary())
    print("repr(journal):", repr(journal))
    print("str(journal):  ", journal)
    print("repr(score_view):", repr(score_view))
    print("repr(s001_view):", repr(s001_view))
