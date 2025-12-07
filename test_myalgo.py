import numpy as np
import sys
import os

sys.path.insert(0, os.getcwd())

try:
    import myalgo
    HAS_MYALGO = True
except ImportError:
    print("ВНИМАНИЕ: Модуль myalgo не найден. Скомпилируйте его сначала!")
    print("Запустите: g++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) -I./src bindings.cpp src/GrayScale.cpp -o myalgo$(python3-config --extension-suffix)")
    HAS_MYALGO = False
    exit(1)

def create_test_image(height=3, width=4):
    """Создаем тестовое RGB изображение"""
    image = []
    for i in range(height):
        row = []
        for j in range(width):
            r = (i * 50 + j * 20) % 256
            g = (i * 30 + j * 40) % 256
            b = (i * 20 + j * 60) % 256
            row.append([float(r), float(g), float(b)])
        image.append(row)
    return image

def manual_grayscale(rgb_image):
    """Ручная реализация для проверки (та же формула)"""
    height = len(rgb_image)
    width = len(rgb_image[0])
    result = []
    
    for i in range(height):
        row = []
        for j in range(width):
            r, g, b = rgb_image[i][j]
            gray = 0.299 * r + 0.587 * g + 0.114 * b
            row.append(gray)
        result.append(row)
    
    return result

def test_basic_conversion():
    """Тест 1: Базовая конвертация"""
    print("Test 1: Basic conversion")
    rgb_image = [
        [[255.0, 0.0, 0.0],
         [0.0, 255.0, 0.0]],
        [[0.0, 0.0, 255.0],
         [255.0, 255.0, 255.0]] 
    ]
    
    # Наша реализация
    our_gray = myalgo.GrayScale.convert_to_gray(rgb_image)
    
    # Ручной расчет
    manual_gray = manual_grayscale(rgb_image)
    
    # Проверяем результаты
    for i in range(2):
        for j in range(2):
            diff = abs(our_gray[i][j] - manual_gray[i][j])
            if diff > 1e-10:
                print(f"  ERROR at ({i},{j}): {our_gray[i][j]} vs {manual_gray[i][j]}")
                return False
    
    # Проверяем конкретные значения
    expected_red = 0.299 * 255
    expected_green = 0.587 * 255
    expected_blue = 0.114 * 255
    expected_white = 255.0
    
    checks = [
        (our_gray[0][0], expected_red, "red"),
        (our_gray[0][1], expected_green, "green"),
        (our_gray[1][0], expected_blue, "blue"),
        (our_gray[1][1], expected_white, "white")
    ]
    
    for value, expected, name in checks:
        diff = abs(value - expected)
        print(f"  {name}: {value:.2f} (expected: {expected:.2f}, diff: {diff:.2e})")
        assert diff < 1e-10, f"{name} pixel mismatch"
    
    print("  ✓ PASSED")
    return True

def test_random_image():
    """Тест 2: Случайное изображение"""
    print("\nTest 2: Random image (5x3)")
    
    # Создаем случайное изображение
    np.random.seed(42)
    height, width = 5, 3
    
    # Генерируем как список списков списков
    rgb_image = []
    for i in range(height):
        row = []
        for j in range(width):
            pixel = list(np.random.randint(0, 256, 3).astype(float))
            row.append(pixel)
        rgb_image.append(row)
    
    # Наша реализация
    our_gray = myalgo.GrayScale.convert_to_gray(rgb_image)
    
    # Ручной расчет
    manual_gray = manual_grayscale(rgb_image)
    
    # Сравниваем
    max_diff = 0
    for i in range(height):
        for j in range(width):
            diff = abs(our_gray[i][j] - manual_gray[i][j])
            max_diff = max(max_diff, diff)
    
    print(f"  Max difference: {max_diff:.2e}")
    
    if max_diff > 1e-10:
        print(f"  ERROR: Large difference detected")
        return False
    
    print("  ✓ PASSED")
    return True

def test_error_handling():
    """Тест 3: Проверка обработки ошибок"""
    print("\nTest 3: Error handling")
    
    # Тест 3.1: Пустое изображение
    try:
        myalgo.GrayScale.convert_to_gray([])
        print("  ERROR: Should have failed on empty image")
        return False
    except Exception as e:
        print(f"  ✓ Correctly rejected empty image: {type(e).__name__}")
    
    # Тест 3.2: Неправильные размеры
    invalid_image = [
        [[1.0, 2.0, 3.0]],
        [[4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]  # Разная ширина
    ]
    
    try:
        myalgo.GrayScale.convert_to_gray(invalid_image)
        print("  ERROR: Should have failed on inconsistent width")
        return False
    except Exception as e:
        print(f"  ✓ Correctly rejected inconsistent width: {type(e).__name__}")
    
    # Тест 3.3: Не 3 канала
    invalid_pixel = [
        [[1.0, 2.0], [3.0, 4.0]]  # Только 2 канала
    ]
    
    try:
        myalgo.GrayScale.convert_to_gray(invalid_pixel)
        print("  ERROR: Should have failed on 2-channel image")
        return False
    except Exception as e:
        print(f"  ✓ Correctly rejected wrong channels: {type(e).__name__}")
    
    print("  ✓ PASSED")
    return True

def test_performance():
    """Тест 4: Производительность"""
    print("\nTest 4: Performance test (100x100 image)")
    
    # Создаем большое изображение
    height, width = 100, 100
    rgb_image = create_test_image(height, width)
    
    import time
    
    # Наша реализация
    start = time.time()
    our_gray = myalgo.GrayScale.convert_to_gray(rgb_image)
    our_time = time.time() - start
    
    # Ручной расчет в Python
    start = time.time()
    manual_gray = manual_grayscale(rgb_image)
    python_time = time.time() - start
    
    # Проверяем, что результаты совпадают
    max_diff = 0
    for i in range(height):
        for j in range(width):
            diff = abs(our_gray[i][j] - manual_gray[i][j])
            max_diff = max(max_diff, diff)
    
    print(f"  C++ implementation: {our_time:.4f} sec")
    print(f"  Pure Python: {python_time:.4f} sec")
    print(f"  Speedup: {python_time/our_time:.2f}x")
    print(f"  Max difference: {max_diff:.2e}")
    
    assert max_diff < 1e-10, "Results don't match"
    print("  ✓ PASSED")
    return True

def main():
    """Основная функция тестирования"""
    print("=" * 60)
    print("Testing myalgo package - Grayscale Conversion")
    print("=" * 60)
    
    tests = [
        test_basic_conversion,
        test_random_image,
        test_error_handling,
        test_performance
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  ✗ FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed successfully!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    exit(main())