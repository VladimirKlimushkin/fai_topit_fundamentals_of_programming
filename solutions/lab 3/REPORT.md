# Лабораторная работа № 3. Алгоритмы, коллекции и функции

## Задание 1. Условия и классификация данных

### Часть 1. Проверка диапазонов

Проверка корректности входных данных выполняется последовательно с помощью `if`. Если хотя бы одно условие нарушено, функция возвращает сообщение об ошибке и не выполняет дальнейшую классификацию (ранний выход через `return`).

```python
if result < 0 or result > 100:
    return "Ошибка: результат должен быть от 0 до 100"
if miss < 0 or miss > 5:
    return "Ошибка: количество пропусков должно быть от 0 до 5"
if work_type not in ("exam", "project", "practice"):
    return "Ошибка: неизвестный тип работы"
```
    
Порядок проверки условий:

Диапазон результата (0–100) — самое критичное значение.

Диапазон пропусков (0–5).

Допустимость типа работы.

Недостижимые ветви при выбранном порядке. Если result вне диапазона, проверки miss и work_type не выполняются — соответствующие им сообщения об ошибке для такого набора данных недостижимы. Аналогично при некорректном miss ветвь проверки work_type не достигается.

Часть 2. Определение уровня результата
Уровень определяется через if / elif / else по убыванию порога (сверху вниз), что позволяет не писать двойные условия вида 60 <= result < 75.

Результат	Уровень
90–100	отличный
75–89	хороший
60–74	удовлетворительный
0–59	недостаточный
Снижение при miss > 3 реализовано через индекс в списке levels: если index > 0, он уменьшается на 1. Для «недостаточного» (index == 0) снижение не происходит — уровень не может стать ниже.

Недостижимые ветви. В цепочке if / elif / else ветвь else достижима только при result < 60, ветви elif result >= 75 и elif result >= 60 — только когда предыдущие условия ложны (соответственно result < 90 и result < 75). Перекрывающихся ветвей нет, все достижимы.

### Часть 3. Сопоставление с образцом (match / case)
```python
def work_description(work_type):
    match work_type:
        case "exam":
            return "экзаменационная работа"
        case "project":
            return "проектная работа"
        case "practice":
            return "практическая работа"
        case _:
            return "неизвестный тип работы"
```

exam - экзаменационная работа;

project - проектная работа;

practice - практическая работа;

_ - неизвестный тип работы.

### Часть 4. Тестовые сценарии
№	score	work_type	miss	Ожидаемый уровень	Фактический
1	0	exam	0	недостаточный	недостаточный
2	59	project	2	недостаточный	недостаточный
3	60	practice	0	удовлетворительный	удовлетворительный
4	74	exam	1	удовлетворительный	удовлетворительный
5	75	project	0	хороший	хороший
6	89	practice	2	хороший	хороший
7	90	exam	0	отличный	отличный
8	100	project	3	отличный	отличный
9	95	practice	4	хороший (снижение)	хороший
10	80	exam	5	удовлетворительный (снижение)	удовлетворительный
11	55	project	4	недостаточный (ниже нельзя)	недостаточный
12	105	exam	0	Ошибка	Ошибка
13	50	exam	6	Ошибка	Ошибка
14	70	test	0	Ошибка	Ошибка
Практическое расширение
Список из 12 записей вида (score, work_type, absences). Для каждой записи формируется строка результата, затем подсчитывается число студентов каждого уровня. Исходный список не изменяется (используется только чтение и локальные счётчики).

```python
records = [
    (95, "exam", 1), (82, "project", 0), (60, "practice", 4),
    (45, "exam", 2), (100, "project", 0), (78, "exam", 5),
    (91, "practice", 3), (30, "exam", 0), (67, "project", 1),
    (88, "practice", 2), (55, "exam", 4), (73, "project", 0),
]

summary = {"недостаточный": 0, "удовлетворительный": 0, "хороший": 0, "отличный": 0}
for score, work_type, miss in records:
    level = student_result(score, work_type, miss)
    summary[level] += 1
    print(f"{score:>3} {work_type:<8} miss={miss} -> {level}")

print("Сводка:", summary)
```

## Задание 2. Циклы и базовые алгоритмические схемы
Исходные данные
```python
measurements = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]
```

Один проход: сумма, минимум, максимум, чётные
```python
def one_pass_stats(data):
    total = 0
    mn = data[0]
    mx = data[0]
    even_count = 0
    for x in data:
        total += x
        if x < mn:
            mn = x
        if x > mx:
            mx = x
        if x % 2 == 0:
            even_count += 1
    return total, mn, mx, even_count
```
    
Сложность: O(n) по времени, O(1) дополнительной памяти. Параметр — длина списка n.

Второй проход: выше среднего
```python
def above_average_count(data, total):
    avg = total / len(data)
    count = 0
    for x in data:
        if x > avg:
            count += 1
    return count, avg
```
    
Сложность: O(n) по времени (второй проход), O(1) памяти. Среднее становится известно только после суммы — поэтому нужен отдельный проход.

Линейный поиск
```python
def linear_search(data, target):
    for i in range(len(data)):
        if data[i] == target:
            return i
    return -1
```
    
Сложность: O(n) в худшем, O(1) в лучшем. Память O(1). Возвращает индекс первого вхождения или -1.

Проверка простоты
```python
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True
```
    
Сложность: O(√n) по времени, O(1) памяти. Почему √n корректно: если n = a * b и a ≤ b, то a ≤ √n. Значит, если делитель существует, среди делителей до √n обязательно найдётся меньший из пары. Перебор только до d * d <= n покрывает все возможные делители.

Практическое расширение: сортировка выбором и бинарный поиск
```python
def selection_sort(data):
    arr = data[:]
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def linear_search_count(data, target):
    comparisons = 0
    for i in range(len(data)):
        comparisons += 1
        if data[i] == target:
            return i, comparisons
    return -1, comparisons

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    comparisons = 0
    while left <= right:
        mid = (left + right) // 2
        comparisons += 1
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1, comparisons
```    

Сложность:

selection_sort — O(n²) по времени, O(n) памяти (копия).

linear_search_count — O(n) сравнений.

binary_search — O(log n) сравнений.

Сравнительная таблица числа сравнений
Целевой элемент отсутствует в массиве (target = -1), поэтому оба алгоритма проходят весь путь до конца.

N	Линейный (сравнений)	Бинарный (сравнений)
10	10	4
100	100	7
1000	1000	10
Линейный поиск делает ровно N сравнений, бинарный — около ⌈log₂(N+1)⌉. На N = 1000 разница в 100 раз, и она растёт с ростом N.

## Задание 3. Коллекции и выбор структуры данных
Исходные данные
```python
submissions = [
    ("anna", "lab_01", 5),
    ("boris", "lab_01", 4),
    ("anna", "lab_02", 5),
    ("daria", "lab_01", 3),
    ("boris", "lab_02", 5),
    ("anna", "lab_01", 4),
]
```
Построенные структуры
Множество студентов: {"anna", "boris", "daria"}.

Множество работ: {"lab_01", "lab_02"}.

Попытки по студенту: словарь name -> [(lab, score), ...].

Лучшие результаты: словарь (name, lab) -> max_score.

Количество попыток: словарь (name, lab) -> count.

```python
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
```
Студенты, сдававшие обе работы
```python
def students_both_labs(submissions, labs):
    labs = sorted(labs)
    if len(labs) < 2:
        return set()
    by_lab = {lab: set() for lab in labs}
    for name, lab, _ in submissions:
        by_lab[lab].add(name)
    return set.intersection(*by_lab.values())
```
Для текущих данных: {"anna", "boris"} — daria сдавала только lab_01.

Добавление записи без полного перестроения
```python
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
```
Добавление ("daria", "lab_02", 4) обновляет все структуры инкрементально, без повторного прохода по всему списку.

**Почему выбраны такие структуры**
Множество для уникальных значений. set хранит только уникальные элементы и обеспечивает среднюю сложность добавления/проверки O(1) за счёт хеширования. Для «списка всех студентов» и «списка всех работ» это идеально: повторы автоматически отбрасываются.

Кортеж как ключ словаря. Кортеж неизменяем и хешируем — значит, его хеш не меняется со временем, и он может быть ключом. (name, lab) — компактный составной ключ, однозначно определяющий пару.

Список нельзя использовать как ключ словаря. Список изменяем: его содержимое может поменяться, а значит поменяется хеш — словарь потеряет возможность найти элемент. Python выбрасывает TypeError: unhashable type: 'list'. Технически это возможно только для неизменяемых типов.

Словарь предпочтительнее списка для частого поиска по ключу. Список ищет перебором — O(n) на запрос. Словарь — O(1) в среднем благодаря хеш-таблице. Для частых запросов «лучший результат по (student, lab)» словарь радикально быстрее.

**Оценка средней сложности**
Коллекция	Добавление	Поиск
set	O(1)	O(1)
dict	O(1)	O(1)
list (append)	O(1)	O(n)
tuple (создание)	O(k) по длине	O(k)
В худшем случае для set/dict возможны коллизии и деградация до O(n), но в среднем — O(1).

Практическое расширение: текстовые запросы
```python
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
```
Примеры работы:

```text
> student anna
Попытки anna: lab_01=5, lab_02=5, lab_01=4

> best anna lab_01
Лучший результат anna по lab_01: 5

> attempts boris lab_02
Попыток boris по lab_02: 1

> completed lab_01
Сдали lab_01: anna, boris, daria

> unknown foo
Неизвестная команда: unknown

> best никто lab_01
Нет данных для никто / lab_01.
Неизвестная команда и отсутствующий ключ обрабатываются без аварийного завершения — возвращается текстовая строка с пояснением.
```

## Задание 4. Функции, параметры и области видимости
Реализованные функции
```python
def arithmetic_mean(values: list[float]) -> float: ...
def normalize_name(name: str) -> str: ...
def build_report(student, results, *, precision=2, prefix="Результат") -> str: ...
def collect_tags(*tags: str, lowercase: bool = True) -> tuple[str, ...]: ...
```
**Требования и как они выполнены**
Требование	Реализация
Не изменять входные коллекции	arithmetic_mean только читает; normalize_name не мутирует строку; build_report не трогает results; collect_tags создаёт новый кортеж
Ранний return при невозможности контракта	raise ValueError при пустых values, пустом name, пустых results (в add_result — создание нового списка)
precision и prefix — только именованные	В сигнатуре build_report стоит * перед ними
Не менее трёх assert на функцию	См. код: у каждой функции ≥ 3 assert (типы входа, инварианты выхода)
Вызовы с позиционными и именованными аргументами	build_report("анна", [5, 5], precision=1), collect_tags("Python", lowercase=False)
Распаковка * и **	build_report("иван", scores, **opts), collect_tags(*tag_list)
**Примеры вызовов и распаковки**
```python
scores = [5, 4, 3]
opts = {"precision": 1, "prefix": "Оценка"}
build_report("иван", scores, **opts)          # Оценка для Иван: 4.0 (оценок: 3)

tag_list = ["Python", " python ", "ML"]
collect_tags(*tag_list)                        # ('python', 'ml')

build_report("анна", [5, 5], prefix="Итог", precision=0)   # Итог для Анна: 5 (оценок: 2)
Исследование LEGB
python
course = "Python-разработчик"      # GLOBAL

def make_greeting(base="Привет"):
    who = "студент"                # ENCLOSING для inner
    def inner(new_who):
        nonlocal who               # меняем who, не course
        who = new_who.strip()
        return f"{base}, {who}!"
    return inner("Иван")
```    

**Схема областей видимости:**

```text
GLOBAL (модуль)
    course = "Python-разработчик"
        ENCLOSING: make_greeting(base="Привет")
          локальные: base, who
            ENCLOSING: inner(new_who)   ← nonlocal who
                локальные: new_who
                BUILTINS: print, isinstance, assert
```
Порядок поиска (LEGB — Local -> Enclosing -> Global -> Builtins):

Имя	Где используется	Найдено в	Как попало / изменение
course	make_greeting	Global	читается, не меняется
base	inner	Enclosing	параметр внешней функции
who	inner	Enclosing	объявлен nonlocal, изменяется
new_who	inner	Local	параметр inner
result	make_greeting	Local	присваивается
print / isinstance	модуль	Builtins	встроенные функции

nonlocal who разрешает присваивание в объемлющую область make_greeting. Глобальное course не тронуто, потому что без global course присваивание из inner создало бы локальную переменную и не затронуло глобальную.

Ошибка изменяемого значения по умолчанию
Исходная функция:

```python
def add_result(value, results=[]):
    results.append(value)
    return results
```
Симптомы:

```python
add_result(1)   # [1]
add_result(2)   # [1, 2]  ← ожидали [2]
add_result(3)   # [1, 2, 3]
```
Объяснение через жизненный цикл значения по умолчанию:

Выражение [] вычисляется один раз — при выполнении def, а не при каждом вызове.

Результат сохраняется в атрибуте функции add_result.__defaults__ = ([],).

При вызове без аргумента Python подставляет ссылку на этот же объект.

results.append(value) мутирует общий объект — следующий вызов видит изменённый список.

Список живёт, пока жива функция; между вызовами он не сбрасывается.

**Исправление:**

```python
def add_result(value, results: Optional[list] = None) -> list:
    if results is None:
        results = []
    return [*results, value]
```
None — неизменяемый маркер «аргумент не передан». Реальный список создаётся внутри вызова — новый объект на каждый вызов. Входной список не мутируется.

Практическое расширение: apply_to_results и make_threshold_checker
```python
def apply_to_results(operation, values):
    return [operation(v) for v in values]

def make_threshold_checker(threshold):
    def check(value):
        return value >= threshold
    return check
```
Передача именованной функции и lambda:

```python
def double(x):
    return x * 2

apply_to_results(double, [1, 2, 3])             # [2, 4, 6]
apply_to_results(lambda x: x ** 2, [1, 2, 3])   # [1, 4, 9]
```
Две независимые проверки:

```python
pass_60 = make_threshold_checker(60)
pass_90 = make_threshold_checker(90)

pass_60(75)   # True
pass_90(75)   # False
pass_90(95)   # True
```
Что сохраняется в замыкании. При вызове make_threshold_checker(60) создаётся локальная переменная threshold = 60 в кадре внешней функции. Вложенная check ссылается на неё; после возврата check кадр не уничтожается полностью — threshold удерживается ячейкой замыкания (check.__closure__[0].cell_contents == 60). Каждый вызов фабрики создаёт свою ячейку: pass_60.__closure__ is pass_90.__closure__ → False. Поэтому проверки с порогами 60 и 90 полностью независимы.

## Задание 5. Анализатор учебных результатов
Исходные данные
```python
students = {
    "Анна": [78, 91, 84, 88],
    "Борис": [60, 72, 68],
    "Дарья": [95, 93, 97, 90],
    "Илья": [55, 61],
}
```
Контракты публичных функций
Функция	Вход	Результат	Особые случаи
mean(values)	непустой список чисел	float	пустой список — ZeroDivisionError (контракт: непустой)
minimum(values)	непустой список чисел	минимум	—
maximum(values)	непустой список чисел	максимум	—
classify(score)	число 0–100	строка категории	границы: 90, 75, 60 включительно
student_summary(name, results)	имя + список оценок	dict	пустой список → mean=None, категория «нет результатов»
group_summary(students)	словарь	dict со сводкой	пустая группа → group_mean=None, leaders=[]
find_top_students(students)	словарь	список имён	пустой вход или все пустые → []
format_report(student_data, group_data)	сводки	строка	—
Декомпозиция
mean, minimum, maximum — атомарные вычисления над одним списком.

classify — чистый маппинг «число → текст».

student_summary — собирает итоги одного студента.

group_summary — агрегирует student_summary по всем студентам и добавляет сводные метрики.

find_top_students — отдельная операция «кто лидер».

format_report — только форматирование, без вычислений.

Каждая функция имеет одну зону ответственности, поэтому её легко тестировать и переиспользовать.

**Оценка сложности**
group_summary вызывает student_summary для каждого студента. Для студента с k оценками student_summary делает три прохода по списку (mean, minimum, maximum) — O(k). Суммарно по группе: O(Σ kᵢ) = O(N), где N — общее число оценок. Дополнительная память — O(m), где m — число студентов (список сводок). Если оценки считать по всем студентам, общая сложность построения статистики — O(N) по времени и O(m) по памяти.

Проверочные сценарии
№	Сценарий	Вход	Ожидаемый результат
1	Обычный набор	исходные students	Анна средний 85.25 (хороший), Дарья лидер 93.75 (отличный), Борис 66.67, Илья 58
2	Один студент	{"Анна": [80]}	mean=80, лидер — Анна
3	Несколько лидеров	{"A": [90], "B": [90], "C": [70]}	find_top_students вернёт ["A", "B"]
4	Пустая группа	{}	count=0, group_mean=None, leaders=[]
5	Студент без результатов	{"A": [], "B": [80]}	у A категория «нет результатов», группа считается по B
6	Границы категорий	{"X": [90], "Y": [75], "Z": [60], "W": [59]}	X — отличный, Y — хороший, Z — удовлетворительный, W — недостаточный
Пример вывода:

```text
==================================================
ОТЧЁТ ПО РЕЗУЛЬТАТАМ ГРУППЫ
==================================================

Студент: Анна
  Оценок: 4
  Средний: 85.25
  Минимум: 78
  Максимум: 91
  Категория: хороший

Студент: Борис
  Оценок: 3
  Средний: 66.67
  Минимум: 60
  Максимум: 72
  Категория: удовлетворительный

Студент: Дарья
  Оценок: 4
  Средний: 93.75
  Минимум: 90
  Максимум: 97
  Категория: отличный

Студент: Илья
  Оценок: 2
  Средний: 58.00
  Минимум: 55
  Максимум: 61
  Категория: недостаточный

--------------------------------------------------
СВОДКА ПО ГРУППЕ
--------------------------------------------------
Всего студентов: 4
Средний балл группы: 75.92
Лучший средний: 93.75
Худший средний: 58.00
Лидеры: Дарья

Распределение по категориям:
  отличный: 1
  хороший: 1
  удовлетворительный: 1
  недостаточный: 1

Топ студентов: ['Дарья']
```

Правило для пустого списка
Студент с [] получает mean=None, min=None, max=None, категорию "нет результатов". В group_summary такие студенты исключаются из расчёта среднего по группе и из поиска лидеров, но учитываются в общем счёте count и в распределении по категориям (как отдельная категория). Это правило задокументировано в контракте student_summary и group_summary.
