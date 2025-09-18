import random
import time


# 1. Генерация отсортированного массива со случайным шагом от 3 до 5
def generate_sorted_array():
    start = 10
    end = 250000000
    step = random.randint(3, 5)
    print(f"Генерируем массив с шагом {step}...")

    # Используем range с randomint для большей рандомизации
    arr = []
    current = start
    while current <= end:
        arr.append(current)
        current += random.randint(3, 5)  # Случайный шаг между элементами

    print(f"Массив сгенерирован. Размер: {len(arr):,} элементов")
    return arr


# 2. Генерация 10 случайных чисел
def generate_random_numbers():
    random_numbers = [random.randint(10, 250000000) for _ in range(10)]
    print(f"Сгенерированы случайные числа: {random_numbers}")
    return random_numbers


# 3. Алгоритм линейного поиска
def linear_search(arr, target):
    for i, num in enumerate(arr):
        if num == target:
            return i
    return -1


# 4. Алгоритм бинарного поиска
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


# Основная функция
def main():
    print("=== ГЕНЕРАЦИЯ ДАННЫХ ===")

    # Генерация массива
    sorted_array = generate_sorted_array()

    # Генерация случайных чисел
    random_numbers = generate_random_numbers()

    print("\n=== ЛИНЕЙНЫЙ ПОИСК ===")
    linear_times = []

    for target in random_numbers:
        start_time = time.time()
        result = linear_search(sorted_array, target)
        end_time = time.time()
        search_time = end_time - start_time
        linear_times.append(search_time)

        status = "найден" if result != -1 else "не найден"
        print(f"Число {target} {status}. Время: {search_time:.6f} сек")

    print(f"\nСреднее время линейного поиска: {sum(linear_times) / len(linear_times):.6f} сек")

    print("\n=== БИНАРНЫЙ ПОИСК ===")
    binary_times = []

    for target in random_numbers:
        start_time = time.time()
        result = binary_search(sorted_array, target)
        end_time = time.time()
        search_time = end_time - start_time
        binary_times.append(search_time)

        status = "найден" if result != -1 else "не найден"
        print(f"Число {target} {status}. Время: {search_time:.6f} сек")

    print(f"\nСреднее время бинарного поиска: {sum(binary_times) / len(binary_times):.6f} сек")

    # Сравнение производительности
    print(f"\n=== СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ ===")
    print(f"Бинарный поиск быстрее линейного в {sum(linear_times) / sum(binary_times):.1f} раз!")


if __name__ == "__main__":
    main()