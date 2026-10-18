import sys
import weakref


data = [1, 2, 3]
print("После создания:", sys.getrefcount(data))

alias = data
print("После создания alias:", sys.getrefcount(data))

container = [data]
print("После помещения в контейнер:", sys.getrefcount(data))

del alias
print("После del alias:", sys.getrefcount(data))

container.clear()
print("После очистки контейнера:", sys.getrefcount(data))



class Record:
    pass


record = Record()
weak_record = weakref.ref(record)

print()
print("Слабые ссылки")
print("weak_record() пока жив:", weak_record())
del record
print("weak_record() после del:", weak_record())

print("\n=== WeakValueDictionary ===")


def make_records():
    r1, r2, r3 = Record(), Record(), Record()
    registry = weakref.WeakValueDictionary()
    registry["one"] = r1
    registry["two"] = r2
    registry["three"] = r3
    return registry, r1, r2


registry, keep1, keep2 = make_records()
print("Состав реестра:", list(registry.keys()))

del keep1
print("После del keep1:", list(registry.keys()))

del keep2
print("После del keep2:", list(registry.keys()))