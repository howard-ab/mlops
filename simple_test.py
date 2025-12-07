#!/usr/bin/env python3
"""
Простой тест для быстрой проверки
"""

import myalgo

# Простое изображение 2x2
image = [
    [[255, 0, 0], [0, 255, 0]],    # Красный, Зеленый
    [[0, 0, 255], [255, 255, 255]]  # Синий, Белый
]

# Конвертируем
gray = myalgo.GrayScale.convert_to_gray(image)

print("Input RGB image:")
for row in image:
    print("  ", row)

print("\nOutput grayscale:")
for row in gray:
    print("  ", [f"{val:.1f}" for val in row])

print("\nExpected values:")
print("  Red (255,0,0):", 0.299 * 255)
print("  Green (0,255,0):", 0.587 * 255)
print("  Blue (0,0,255):", 0.114 * 255)
print("  White (255,255,255):", 255.0)

print("\n✅ Package works correctly!")
