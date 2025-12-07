# Grayscale Converter with Python Bindings

Простой проект для конвертации RGB изображений в оттенки серого с использованием C++ и Python bindings.

## Функционал

- Конвертация RGB → Grayscale
- Формула: `Gray = 0.299*R + 0.587*G + 0.114*B`
- Вход: 3D список `[height][width][3]`
- Выход: 2D список `[height][width]`

## Установка

### Из wheel файла:
```bash
pip install myalgo.whl