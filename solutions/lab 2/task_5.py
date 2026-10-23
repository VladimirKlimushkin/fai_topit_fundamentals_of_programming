import sys
import tracemalloc
import gc


def kb(b):
    return b / 1024


objects = {
    "пустой список": [],
    "список из 10 int": list(range(10)),
    "кортеж из 10 int": tuple(range(10)),
    "строка из 10 символов": "0123456789",
    "целое число": 12345,
    "None": None,
}
for label, obj in objects.items():
    print(f"{label:25} {sys.getsizeof(obj):5} байт")

lst = []
last_size = sys.getsizeof(lst)
print(f"len=0, size={last_size}")
for i in range(100):
    lst.append(i)
    size = sys.getsizeof(lst)
    if size != last_size:
        print(f"len={len(lst)}, size={size}")
        last_size = size


def measure(label, factory):
    gc.collect()
    tracemalloc.start()
    obj = factory()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{label}: current={kb(current):.1f} КБ, peak={kb(peak):.1f} КБ")
    return current, peak


cur1, peak1 = measure("list(range(100_000))", lambda: list(range(100_000)))
cur2, peak2 = measure("range(100_000)", lambda: range(100_000))

print()
print(f"Отношение peak: {peak1 / peak2:.1f}x")