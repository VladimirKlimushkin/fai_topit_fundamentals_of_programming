a = 10
b = a

print(a, b)
print(id(a), id(b))

a += 1

print(a, b)
print(id(a), id(b))

first = [10, 20]
second = first

print(first, second)
print(id(first), id(second))

second.append(30)

print(first, second)
print(id(first), id(second))

second = [10, 20, 30]  # переназначение на новый список
print(first == second) # значения равны
print(first is second) # разные объекты

second.append(40)  # меняем новый список
print(first)  # first не изменился
print(second)  # [10, 20, 30, 40]


config1 = {
    "name": "Проект А",
    "members": ["Аня", "Боря"],
    "params": ["--debug", "--verbose"],
}

config2 = config1
config2["members"].append("Вика")
print(config1["members"])  # ['Аня', 'Боря', 'Вика']

import copy
config3 = copy.deepcopy(config1)
config3["members"].append("Гриша")
assert config1["members"] != config3["members"]
print(config1["members"] is config2["members"])  # True — общий объект
print(config1["members"] is config3["members"])  # False — независимые