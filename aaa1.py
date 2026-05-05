import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")

        #дание виджетов интерфейса
        self.create_widgets()

        # Список для хранения записей
        self.entries = []

        # Загрузка данных из файла
        self.load_data()

    def create_widgets(self):
        # Поля ввода
        self.date_label = tk.Label(self.root, text="Дата (YYYY-MM-DD):")
        self.date_label.pack()
        self.date_entry = tk.Entry(self.root)
        self.date_entry.pack()

        self.temp_label = tk.Label(self.root, text="Температура (°C):")
        self.temp_label.pack()
        self.temp_entry = tk.Entry(self.root)
        self.temp_entry.pack()

        self.desc_label = tk.Label(self.root, text="Описание погоды:")
        self.desc_label.pack()
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.pack()

        self.precipitation_var = tk.BooleanVar()
        self.precipitation_check = tk.Checkbutton(self.root, text="Осадки?", variable=self.precipitation_var)
        self.precipitation_check.pack()

        # Кнопки
        self.add_button = tk.Button(self.root, text="Добавить запись", command=self.add_entry)
        self.add_button.pack()

        self.filter_button = tk.Button(self.root, text="Фильтровать записи", command=self.filter_entries)
        self.filter_button.pack()

        # Список для отображения записей
        self.notes_listbox = tk.Listbox(self.root, width=50)
        self.notes_listbox.pack()

    def add_entry(self):
        date = self.date_entry.get()
        temp = self.temp_entry.get()
        desc = self.desc_entry.get()
        precip = self.precipitation_var.get()

        if self.validate_input(date, temp, desc):
            entry = {
                "date": date,
                "temperature": float(temp),
                "description": desc,
                "precipitation": precip
            }
            self.entries.append(entry)
            self.update_listbox()
            self.save_data()
            self.clear_entries()
        else:
            messagebox.showerror("Ошибка ввода", "Пожалуйста, проверьте введенные данные.")

    def validate_input(self, date, temp, desc):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            if not (-100 <= float(temp) <= 100):  # Проверка диапазона температуры
                return False
            if not desc.strip():
                return False
            return True
        except ValueError:
            return False

    def update_listbox(self):
        self.notes_listbox.delete(0, tk.END)
        for entry in self.entries:
            self.notes_listbox.insert(tk.END, f"{entry['date']}: {entry['description']} ({entry['temperature']}°C, {'Yes' if entry['precipitation'] else 'No'})")

    def filter_entries(self):
        criteria = simpledialog.askstring("Фильтр", "Введите минимальную температуру:")
        if criteria:
            try:
                criteria = float(criteria)
                filtered_entries = [entry for entry in self.entries if entry["temperature"] > criteria]
                self.notes_listbox.delete(0, tk.END)
                for entry in filtered_entries:
                    self.notes_listbox.insert(tk.END, f"{entry['date']}: {entry['description']} ({entry['temperature']}°C, {'Yes' if entry['precipitation'] else 'No'})")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректное значение температуры.")

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precipitation_var.set(False)

    def save_data(self):
        with open('weather_entries.json', 'w') as f:
            json.dump(self.entries, f)

    def load_data(self):
        if os.path.exists('weather_entries.json'):
            with open('weather_entries.json', 'r') as f:
                self.entries = json.load(f)
                self.update_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
