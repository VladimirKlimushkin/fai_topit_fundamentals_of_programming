    def student_result(result, work_type, miss):
        levels = ["недостаточный", "удовлетворительный", "хороший", "отличный"]
        index = 0
        if result < 0 or result > 100:
            return "Ошибка: результат должен быть от 0 до 100"
        if miss < 0 or miss > 5:
            return "Ошибка: количество пропусков должно быть от 0 до 5"
        if work_type not in ("exam", "project", "practice"):
            return "Ошибка: неизвестный тип работы"

        if result >= 90:
            index = 3
        elif result >= 75:
            index = 2
        elif result >= 60:
            index = 1
        else:
            index = 0

        if miss > 3:
            if index > 0:
                index -= 1
        level = levels[index]

        return level


    if __name__ == "__main__":
        result = int(input("Введите результат (0-100): "))
        work_type = input("Введите тип работы (exam/project/practice): ")
        miss = int(input("Введите количество пропусков (0-5): "))

        print(student_result(result, work_type, miss))
