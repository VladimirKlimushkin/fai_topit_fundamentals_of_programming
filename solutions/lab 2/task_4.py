import gc


first = []
second = []
first.append(second)
second.append(first)

print("first ссылается на second:", first[0] is second)
print("second ссылается на first:", second[0] is first)

print("gc.isenabled():", gc.isenabled())
print("Пороги поколений:", gc.get_threshold())
print("Статистика:", gc.get_stats())

ids_before = (id(first), id(second))
print("id до удаления:", ids_before)

del first, second

collected = gc.collect()
print("gc.collect() собрал объектов:", collected)

gc.disable()
print("gc.isenabled():", gc.isenabled())

cycles = []
for _ in range(5):
    a = {}
    b = {}
    a["b"] = b
    b["a"] = a
    cycles.append(a)

del a, b, cycles
print("Создали 5 циклов, удалили внешние ссылки")

n = gc.collect()
print("Собрано вручную:", n)

gc.enable()
print("gc.isenabled() после enable:", gc.isenabled())

gc.collect()
before = gc.collect()
print("Собрано до графа:", before)

n1 = {"name": "n1"}
n2 = {"name": "n2"}
n3 = {"name": "n3"}
n4 = {"name": "n4"}

n1["next"] = n2
n2["next"] = n3
n3["next"] = n1
n4["next"] = None

print("n1 -> n2:", n1["next"] is n2)
print("n2 -> n3:", n2["next"] is n3)
print("n3 -> n1:", n3["next"] is n1)
print("n4 независим:", n4["next"] is None)

del n1, n2, n3
after = gc.collect()
print("Собрано после удаления цикла:", after)

print("n4 доступен:", n4)