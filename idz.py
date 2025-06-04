import numpy as np
import json

# Функція для виведення меню
def menu():
    print("Оберіть завдання:")
    print("1. Сума векторів")
    print("2. Скалярний добуток векторів")
    print("3. Матричний добуток")
    print("4. Обернена матриця")
    print("5. Розв'язання системи лінійних рівнянь")
    print("0. Вийти")

# Функція для введення вектору з клавіатури
def input_vector(prompt):
    while True:
        try:
            # Введення вектору та перевірка на коректність
            vector = np.array([float(x) for x in input(prompt).split()])
            return vector
        except ValueError:
            print("Некоректний ввід. Будь ласка, введіть числа через пробіл.")

# Функція для введення матриці з клавіатури
def input_matrix(prompt):
    while True:
        try:
            # Введення матриці та перевірка на коректність
            rows, cols = map(int, input(prompt).split())
            matrix = np.array([list(map(float, input().split())) for _ in range(rows)])
            return matrix
        except ValueError:
            print("Некоректний ввід. Будь ласка, введіть розмірність та числа матриці коректно.")

# Функція для збереження результату у JSON-файл
def save_to_JSON(result, comment):
    save_option = input("Зберегти результат в JSON-файл? (Так/Ні): ").strip().lower()

    # Перевірка, чи користувач обрав збереження в JSON-файл
    if save_option == "так":
        filename = input("Введіть ім'я JSON-файлу для збереження (з розширенням .json): ").strip()

        if isinstance(result, np.ndarray):
            result_data = result.tolist()
        else:
            result_data = result

        data = {"comment": comment, "result": result_data}

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)

        print(f"Результат збережено у файл {filename}")
    else:
        print("Результат не збережено.")

# Функція для обчислення суми векторів
def sum_vectors():
    print("Введіть координати двох векторів для їх суми:")
    vector1 = input_vector("Перший вектор (введіть числа через пробіл): ")
    vector2 = input_vector("Другий вектор (введіть числа через пробіл): ")

    # Перевірка довжин векторів
    if len(vector1) != len(vector2):
        print("Помилка: Вектори мають різну довжину. Сумування неможливе.")
        return
      
    result = vector1 + vector2
    print("Сума векторів:", result)
    save_to_JSON(result, "Сума векторів")

# Функція для обчислення скалярного добутку векторів
def dot_product():
    print("Введіть координати двох векторів для їх скалярного добутку:")
    vector1 = input_vector("Перший вектор (введіть числа через пробіл): ")
    vector2 = input_vector("Другий вектор (введіть числа через пробіл): ")

    result = np.dot(vector1, vector2)
    print("Скалярний добуток векторів:", result)
    save_to_JSON([result], "Скалярний добуток векторів")

# Функція для обчислення матричного добутку
def matrix_product():
    print("Введіть розмірність першої матриці та її елементи:")
    matrix1 = input_matrix("Розмірність (спочатку введіть рядки та стовпці через пробіл, а з нового рядка елементи матриці): ")

    print("Введіть розмірність другої матриці та її елементи:")
    matrix2 = input_matrix("Розмірність (спочатку введіть рядки та стовпці через пробіл, а з нового рядка елементи матриці): ")

    try:
        result = np.dot(matrix1, matrix2)
        print("Матричний добуток матриць:")
        print(result)
        save_to_JSON(result, "Матричний добуток матриць")
    except ValueError:
        print("Некоректна розмірність для матричного множення.")

# Функція для обчислення оберненої матриці
def inverse_matrix():
    print("Введіть розмірність квадратної матриці та її елементи:")
    matrix = input_matrix("Розмірність (спочатку введіть рядки та стовпці через пробіл, а з нового рядка елементи матриці): ")

    try:
      #обчислює номер умови матриці. Якщо число умови дуже велике, це означає, що матриця близька до сингулярної.
      condition_number = np.linalg.cond(matrix)
      if condition_number > 1/np.finfo(float).eps:
        raise ValueError("Матриця є сингулярною. Обернена матриця не існує.")

      inverse = np.linalg.inv(matrix)
      print("Обернена матриця:")
      print(inverse)
      save_to_JSON(inverse, "Обернена матриця")
    except ValueError as e:
      print(e)

# Функція для розв'язання системи лінійних рівнянь
def solve_linear_system():
    print("Введіть кількість рівнянь та невідомих, а потім коефіцієнти та константи:")
    coefficients = input_matrix("Кількість рівнянь та невідомих через пробіл, з нових рядків коефіцієнти для рівнянь, також через пробіл: ")

    try:
        constants = np.array([float(x) for x in input("Константи рівнянь через пробіл: ").split()])
        solution = np.linalg.solve(coefficients, constants)
        print("Розв'язок системи лінійних рівнянь:")
        print(solution)
        save_to_JSON(solution, "Розв'язок системи лінійних рівнянь")
    except ValueError:
        print("Некоректна розмірність для системи лінійних рівнянь.")
    except np.linalg.LinAlgError:
        print("Система лінійних рівнянь не має розв'язку або має нескінченну кількість розв'язків.")

if __name__ == "__main__":
  while True:
    # Виведення меню для користувача
      menu()
      choice = input("Ваш вибір: ")

      if choice == "1":
          sum_vectors()
      elif choice == "2":
          dot_product()
      elif choice == "3":
          matrix_product()
      elif choice == "4":
          inverse_matrix()
      elif choice == "5":
          solve_linear_system()
      elif choice == "0":
          print("Програма завершена.")
          break
      else:
          print("Невірний вибір. Спробуйте ще раз.")
