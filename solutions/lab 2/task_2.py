import copy


def show(label, structure):
    print(f"{label}: {structure}")


original = [
    ["Python", 5],
    ["Algorithms", 4],
]

alias = original
shallow = original.copy()
deep = copy.deepcopy(original)

print("Before")
for label, s in [("original", original), ("alias", alias),
                 ("shallow", shallow), ("deep", deep)]:
    show(label, s)
    print(f" id внешнего: {id(s)}")
    print(f" id первого вложенного: {id(s[0])}")

print()
print("append 5 to \"Databases\")")
original.append(["Databases", 5])
for label, s in [("original", original), ("alias", alias),
                 ("shallow", shallow), ("deep", deep)]:
    show(label, s)

print()
print("original[0][1] = 3")
original[0][1] = 3
for label, s in [("original", original), ("alias", alias),
                 ("shallow", shallow), ("deep", deep)]:
    show(label, s)

print()
print("First list ID")
for label, s in [("original", original), ("alias", alias),
                 ("shallow", shallow), ("deep", deep)]:
    print(f"{label}: id(s[0]) = {id(s[0])}")

print()
wrong_matrix = [[0] * 3] * 3
wrong_matrix[0][0] = 1
print("wrong_matrix:", wrong_matrix)
print("id строк:", [id(row) for row in wrong_matrix])

print()
correct_matrix = [[0] * 3 for _ in range(3)]
correct_matrix[0][0] = 1
print("correct_matrix:", correct_matrix)
print("id строк:", [id(row) for row in correct_matrix])