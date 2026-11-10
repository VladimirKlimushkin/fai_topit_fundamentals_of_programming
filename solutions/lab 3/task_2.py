measurements = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]

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

def above_average_count(data, total):
    avg = total / len(data)
    count = 0
    for x in data:
        if x > avg:
            count += 1
    return count, avg

def linear_search(data, target):
    for i in range(len(data)):
        if data[i] == target:
            return i
    return -1

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


def linear_search_count(data, target):
    comparisons = 0
    for i in range(len(data)):
        comparisons += 1
        if data[i] == target:
            return i, comparisons
    return -1, comparisons


if __name__ == "__main__":
    print("=" * 60)
    print("Часть 1–2. Статистика списка measurements")
    print("=" * 60)
    total, mn, mx, even_count = one_pass_stats(measurements)
    above, avg = above_average_count(measurements, total)
    print(f"Сумма:               {total}")
    print(f"Минимум:             {mn}")
    print(f"Максимум:            {mx}")
    print(f"Чётных значений:     {even_count}")
    print(f"Среднее арифметич.:  {avg:.2f}")
    print(f"Выше среднего:       {above}")

    print()
    print("=" * 60)
    print("Часть 3. Линейный поиск первого вхождения")
    print("=" * 60)
    try:
        target = int(input("Введите число для поиска: "))
        idx = linear_search(measurements, target)
        print(f"Индекс первого вхождения: {idx}")
    except ValueError:
        print("Некорректный ввод — поиск пропущен.")

    print()
    print("=" * 60)
    print("Часть 4. Проверка простоты")
    print("=" * 60)
    test_numbers = [1, 2, 3, 4, 17, 25, 29, 49, 97, 100, 101]
    for n in test_numbers:
        print(f"{n:>4}: {'простое' if is_prime(n) else 'составное'}")

    print()
    print("=" * 60)
    print("Практическое расширение: сравнение линейного и бинарного поиска")
    print("=" * 60)
    import random
    random.seed(42)

    print(f"{'N':>6} | {'Линейный (сравн.)':>18} | {'Бинарный (сравн.)':>18}")
    print("-" * 52)

    for n in (10, 100, 1000):
        data = sorted(random.randint(0, n * 2) for _ in range(n))
        target = -1
        _, lin_cmp = linear_search_count(data, target)
        _, bin_cmp = binary_search(data, target)
        print(f"{n:>6} | {lin_cmp:>18} | {bin_cmp:>18}")
