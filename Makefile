.PHONY: all clean build test docker-build

# Основные цели
all: build test

# Компиляция с pybind11
build:
	@echo "=== Building with pybind11 ==="
	g++ -O3 -Wall -shared -std=c++11 -fPIC \
		$(shell python3 -m pybind11 --includes) \
		-I./src \
		bindings.cpp src/GrayScale.cpp \
		-o myalgo$(shell python3-config --extension-suffix)
	@echo "✅ Build completed: myalgo$$(python3-config --extension-suffix)"

# Компиляция с CMake
cmake-build:
	@echo "=== Building with CMake ==="
	mkdir -p build
	cd build && cmake .. && make
	@echo "✅ CMake build completed"

# Очистка
clean:
	rm -f *.so
	rm -rf build/ dist/ *.egg-info/
	rm -f *.whl
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Тестирование
test:
	@echo "=== Running tests ==="
	python3 test_myalgo.py

# Сборка Python пакета
package:
	@echo "=== Building Python package ==="
	python3 -m build --wheel
	@echo "✅ Wheel created: dist/myalgo-*.whl"

# Docker сборка
docker-build:
	@echo "=== Building Docker image ==="
	docker build -t myalgo-package .
	@echo "✅ Docker image created: myalgo-package"

# Запуск тестов в Docker
docker-test:
	docker run --rm myalgo-package

# Сборка wheel в Docker и копирование на хост
docker-wheel:
	docker build -t myalgo-package .
	docker run --rm -v $(PWD):/output myalgo-package sh -c "cp /app/myalgo_package.whl /output/"

# Установка локально
install:
	pip install -e .
