
import json
import os
import sys # Для более чистого выхода

# Имя файла для хранения данных
DATA_FILE = "todo_data.json"

def load_tasks():
    """
    Загружает задачи из файла.
    Возвращает список задач или пустой список, если файл не существует или пуст.
    """
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
            # Проверка структуры загруженных данных
            if not isinstance(tasks, list):
                print(f"Предупреждение: Файл {DATA_FILE} имеет некорректный формат. Создан новый пустой список.")
                return []
            for task in tasks:
                if not isinstance(task, dict) or 'description' not in task or 'completed' not in task:
                    print(f"Предупреждение: Задача в файле {DATA_FILE} имеет некорректный формат. Пропускаем.")
                    # Можно удалить некорректную задачу или просто пропустить
            return tasks
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON из файла {DATA_FILE}. Файл поврежден или пуст. Создан новый пустой список.")
        return []
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при загрузке задач: {e}")
        return []

def save_tasks(tasks):
    """
    Сохраняет задачи в файл.
    Использует JSON для структурированного хранения.
    """
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Ошибка записи в файл {DATA_FILE}: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при сохранении задач: {e}")

def display_tasks(tasks):
    """
    Отображает список задач в удобном для пользователя формате.
    Включает нумерацию и статус выполнения (чекбокс).
    """
    if not tasks:
        print("\nВаш список дел пуст. Добавьте первую задачу!")
        return False # Возвращаем False, если список пуст, чтобы основное меню не предлагало действия с пустым списком

    print("\n--- Ваш список дел ---")
    for i, task in enumerate(tasks):
        # Используем символы, похожие на чекбоксы
        status_symbol = "✅" if task.get("completed", False) else "⬜"
        print(f"{i + 1}. {status_symbol} {task.get('description', 'Без описания')}")
    print("----------------------")
    return True # Возвращаем True, если список не пуст

def add_task(tasks):
    """
    Добавляет новую задачу в список.
    Запрашивает описание у пользователя и устанавливает статус 'не выполнено'.
    """
    description = input("Введите описание новой задачи: ").strip()
    if description:
        tasks.append({"description": description, "completed": False})
        save_tasks(tasks)
        print(f"✅ Задача '{description}' добавлена!")
    else:
        print("❌ Описание задачи не может быть пустым.")

def mark_task_complete(tasks):
    """
    Отмечает задачу как выполненную.
    Запрашивает номер задачи у пользователя.
    """
    if not display_tasks(tasks): # Если список пуст, выходим
        return

    try:
        task_number_str = input("Введите номер задачи для отметки как выполненной (или 'отмена' для выхода): ").strip().lower()
        if task_number_str == 'отмена':
            print("Действие отменено.")
            return

        task_number = int(task_number_str)
        if 1 <= task_number <= len(tasks):
            if tasks[task_number - 1]["completed"]:
                print(f"ℹ️ Задача №{task_number} уже была отмечена как выполненная.")
            else:
                tasks[task_number - 1]["completed"] = True
                save_tasks(tasks)
                print(f"✅ Задача №{task_number} отмечена как выполненная!")
        else:
            print(f"❌ Неверный номер задачи. Пожалуйста, введите число от 1 до {len(tasks)}.")
    except ValueError:
        print("❌ Неверный ввод. Пожалуйста, введите число или 'отмена'.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при отметке задачи: {e}")

def delete_task(tasks):
    """
    Удаляет задачу из списка.
    Запрашивает номер задачи у пользователя.
    """
    if not display_tasks(tasks):
        return

    try:
        task_number_str = input("Введите номер задачи для удаления (или 'отмена' для выхода): ").strip().lower()
        if task_number_str == 'отмена':
            print("Действие отменено.")
            return

        task_number = int(task_number_str)
        if 1 <= task_number <= len(tasks):
            removed_task = tasks.pop(task_number - 1)
            save_tasks(tasks)
            print(f"🗑️ Задача №{task_number} ('{removed_task.get('description', 'Без описания')}') удалена.")
        else:
            print(f"❌ Неверный номер задачи. Пожалуйста, введите число от 1 до {len(tasks)}.")
    except ValueError:
        print("❌ Неверный ввод. Пожалуйста, введите число или 'отмена'.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при удалении задачи: {e}")


def main():
    """
    Основная функция программы. Управляет циклом меню и вызовом других функций.
    """
    tasks = load_tasks()

    print("Добро пожаловать в ваш личный менеджер списка дел!")

    while True:
        print("\n--- Главное меню ---")
        print("1. 📋 Показать список дел")
        print("2. ➕ Добавить новую задачу")
        print("3. ✅ Отметить задачу как выполненную")
        print("4. 🗑️ Удалить задачу")
        print("5. 🚪 Выйти")

        choice = input("Выберите действие (1-5): ").strip()

        if choice == '1':
            display_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            mark_task_complete(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            print("Спасибо за использование менеджера списка дел. До свидания!")
            sys.exit(0) # Чистый выход
        else:
            print("❌ Неверный ввод. Пожалуйста, выберите действие от 1 до 5.")

if __name__ == "__main__":
    main()
