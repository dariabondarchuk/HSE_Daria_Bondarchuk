import random
import time

# 1. Сгенерировать массив с шагом от 3 до 5
def generate_sorted_array(start=10, end=250_000_000):
    arr = []
    current = start
    while current <= end:
        arr.append(current)
        current += random.randint(3, 5)
    return arr

# 2. Сгенерировать 10 случайных чисел
random_numbers = [random.randint(10, 250_000_000) for _ in range(10)]

# 3. Линейный поиск
def linear_search(arr, target):
    for i, num in enumerate(arr):
        if num == target:
            return i
    return -1

# 4. Бинарный поиск
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

# ==========================
# Основная программа
# ==========================
print("Генерация массива...")
sorted_array = generate_sorted_array()
print(f"Размер массива: {len(sorted_array):,}")

print("\nСлучайные числа:", random_numbers)

# Проверяем линейный и бинарный поиск
for num in random_numbers:
    print(f"\nИщем число {num}:")

    start = time.time()
    idx_lin = linear_search(sorted_array, num)
    lin_time = time.time() - start

    start = time.time()
    idx_bin = binary_search(sorted_array, num)
    bin_time = time.time() - start

    print(f"Линейный поиск: индекс={idx_lin}, время={lin_time:.6f} сек")
    print(f"Бинарный поиск: индекс={idx_bin}, время={bin_time:.6f} сек")