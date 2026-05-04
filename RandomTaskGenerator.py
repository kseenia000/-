
import tkinter as tk
from tkinter import messagebox
import random
import json
import os

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных задач")
        self.root.geometry("500x400")

        self.tasks = {
            "учеба": ["Прочитать главу учебника", "Решить 5 задач по математике", "Написать конспект лекции"],
            "спорт": ["Сделать зарядку", "Пробежать 3 км", "Посетить спортзал"],
            "работа": ["Ответить на важные письма", "Составить план на день", "Подготовить отчет"]
        }
        self.all_tasks_history = []
        self.history_file = "task_history.json"
        self.load_history()

        self.create_widgets()

    def create_widgets(self):
        # --- Верхняя часть: Заголовок и выбор типа задачи ---
        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=10)

        tk.Label(title_frame, text="Генератор случайных задач", font=("Arial", 16, "bold")).pack()

        type_frame = tk.Frame(self.root)
        type_frame.pack(pady=10)

        tk.Label(type_frame, text="Тип задачи:").pack(side=tk.LEFT, padx=5)
        self.task_type_var = tk.StringVar(self.root)
        self.task_type_var.set("все") # Значение по умолчанию
        task_types = ["все"] + list(self.tasks.keys())
        self.task_type_menu = tk.OptionMenu(type_frame, self.task_type_var, *task_types)
        self.task_type_menu.pack(side=tk.LEFT)
        self.task_type_menu.bind("<Configure>", lambda event: self.task_type_menu.config(width=10)) # Установка ширины

        # --- Центральная часть: Отображение задачи и кнопка генерации ---
        task_display_frame = tk.Frame(self.root, padx=20, pady=20, relief=tk.GROOVE, borderwidth=2)
        task_display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.task_label = tk.Label(task_display_frame, text="Ваша задача появится здесь", font=("Arial", 12), wraplength=350, justify=tk.CENTER)
        self.task_label.pack(expand=True)

        generate_button = tk.Button(self.root, text="Сгенерировать задачу", command=self.generate_task, font=("Arial", 12))
        generate_button.pack(pady=10)

        # --- Нижняя часть: Добавление задач и история ---
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=10, fill=tk.X, padx=20)

        add_task_frame = tk.LabelFrame(bottom_frame, text="Добавить новую задачу", padx=10, pady=10)
        add_task_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        tk.Label(add_task_frame, text="Тип:").grid(row=0, column=0, sticky=tk.W)
        self.new_task_type_entry = tk.Entry(add_task_frame, width=15)
        self.new_task_type_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(add_task_frame, text="Задача:").grid(row=1, column=0, sticky=tk.W)
        self.new_task_entry = tk.Entry(add_task_frame, width=30)
        self.new_task_entry.grid(row=1, column=1, padx=5, pady=2)

        add_button = tk.Button(add_task_frame, text="Добавить", command=self.add_custom_task)
        add_button.grid(row=2, column=0, columnspan=2, pady=5)

        history_button = tk.Button(bottom_frame, text="Показать историю", command=self.show_history)
        history_button.pack(side=tk.RIGHT, padx=10)

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.all_tasks_history = json.load(f)
            except json.JSONDecodeError:
                self.all_tasks_history = []
            except Exception as e:
                print(f"Ошибка при загрузке истории: {e}")
                self.all_tasks_history = []
        else:
            self.all_tasks_history = []

    def save_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.all_tasks_history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении истории: {e}")

    def generate_task(self):
        selected_type = self.task_type_var.get()

        available_tasks = []
        if selected_type == "все":
            for task_list in self.tasks.values():
                available_tasks.extend(task_list)
        elif selected_type in self.tasks:
            available_tasks = self.tasks[selected_type]

        if not available_tasks:
            messagebox.showinfo("Информация", "Нет доступных задач для выбранного типа.")
            self.task_label.config(text="Нет доступных задач.")
            return

        chosen_task = random.choice(available_tasks)
        self.task_label.config(text=chosen_task)

        # Добавляем задачу в историю, если она не пустая
        if chosen_task:
            self.all_tasks_history.append({"type": selected_type, "task": chosen_task})
            self.save_history()

    def add_custom_task(self):
        task_type = self.new_task_type_entry.get().strip().lower()
        task_description = self.new_task_entry.get().strip()

        if not task_type or not task_description:
            messagebox.showwarning("Внимание", "Пожалуйста, введите тип задачи и ее описание.")
            return

        if task_type not in self.tasks:
            self.tasks[task_type] = []

        if task_description not in self.tasks[task_type]:
            self.tasks[task_type].append(task_description)
            # Обновляем OptionMenu
            task_types = ["все"] + list(self.tasks.keys())
            self.task_type_menu["menu"].delete(0, "end")
            for type_ in task_types:
                self.task_type_menu["menu"].add_command(label=type_, command=lambda value=type_: self.task_type_var.set(value))
            self.task_type_var.set(task_type) # Устанавливаем новый тип как выбранный

            self.new_task_type_entry.delete(0, tk.END)
            self.new_task_entry.delete(0, tk.END)
            messagebox.showinfo("Успех", f"Задача '{task_description}' типа '{task_type}' добавлена.")
        else:
            messagebox.showwarning("Внимание", "Такая задача уже существует для этого типа.")


    def show_history(self):
        if not self.all_tasks_history:
            messagebox.showinfo("История задач", "История задач пуста.")
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("История задач")
        history_window.geometry("400x300")

        history_text = tk.Text(history_window, wrap=tk.WORD, padx=10, pady=10)
        history_text.pack(expand=True, fill=tk.BOTH)

        for entry in self.all_tasks_history:
            history_text.insert(tk.END, f"Тип: {entry['type']}, Задача: {entry['task']}\n")
        history_text.config(state=tk.DISABLED) # Делаем текст только для чтения

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
