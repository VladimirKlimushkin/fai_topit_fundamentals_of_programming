import sys
import tracemalloc
import gc


def kb(x):
    return x / 1024


def scenario_list(n):
    gc.collect()
    tracemalloc.start()
    obj = list(range(n))
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "name": "list(range(n))",
        "n": n,
        "size": sys.getsizeof(obj),
        "current_kb": kb(current),
        "peak_kb": kb(peak),
    }


def scenario_range(n):
    gc.collect()
    tracemalloc.start()
    obj = range(n)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "name": "range(n)",
        "n": n,
        "size": sys.getsizeof(obj),
        "current_kb": kb(current),
        "peak_kb": kb(peak),
    }


N = 100_000
results = [scenario_list(N), scenario_range(N)]

ratio = results[0]["peak_kb"] / results[1]["peak_kb"]

print(f"{'Сценарий':<18}{'N':>8}{'Size':>10}{'Current, КБ':>15}{'Peak, КБ':>12}")
for r in results:
    print(f"{r['name']:<18}{r['n']:>8}{r['size']:>10}"
          f"{r['current_kb']:>15.1f}{r['peak_kb']:>12.1f}")
    
print()
print(f"Отношение пиковой памяти list/range: {ratio:.1f}x")