import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "weather_history.json"

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.root.geometry("750x550")

        self.history = self.load_data()

        # --- Форма ввода ---
        input_frame = tk.LabelFrame(root, text="Новая запись", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0)
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))
        self.date_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Температура (°C):").grid(row=0, column=2)
        self.temp_entry = tk.Entry(input_frame)
        self.temp_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Описание:").grid(row=1, column=0, pady=10)
        self.desc_entry = tk.Entry(input_frame, width=30)
        self.desc_entry.grid(row=1, column=1, columnspan=2, padx=5)

        self.precip_var = tk.BooleanVar()
        tk.Checkbutton(input_frame, text="Осадки", variable=self.precip_var).grid(row=1, column=3)

        tk.Button(input_frame, text="Добавить запись", command=self.add_entry, bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=4, sticky="we")

        # --- Блок фильтрации ---
        filter_frame = tk.LabelFrame(root, text="Фильтры", padx=10, pady=5)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Мин. темп:").grid(row=0, column=0)
        self.filter_temp_entry = tk.Entry(filter_frame, width=10)
        self.filter_temp_entry.grid(row=0, column=1, padx=5)

        tk.Button(filter_frame, text="Показать теплее", command=self.filter_temp).grid(row=0, column=2, padx=5)
        tk.Button(filter_frame, text="Сбросить", command=self.refresh_table).grid(row=0, column=3, padx=5)

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("Date", "Temp", "Desc", "Precip"), show="headings")
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Temp", text="Температура")
        self.tree.heading("Desc", text="Описание")
        self.tree.heading("Precip", text="Осадки")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_table()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return []
        return []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def add_entry(self):
        date_str = self.date_entry.get().strip()
        temp_str = self.temp_entry.get().strip()
        desc = self.desc_entry.get().strip()
        precip = "Да" if self.precip_var.get() else "Нет"

        # Валидация
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Формат даты: ДД.ММ.ГГГГ")
            return

        try:
            temp_val = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом")
            return

        if not desc:
            messagebox.showerror("Ошибка", "Описание не может быть пустым")
            return

        self.history.append({
            "date": date_str,
            "temp": temp_val,
            "desc": desc,
            "precip": precip
        })
        self.save_data()
        self.refresh_table()
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

    def refresh_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        display_data = data if data is not None else self.history
        for item in display_data:
            self.tree.insert("", tk.END, values=(item["date"], item["temp"], item["desc"], item["precip"]))

    def filter_temp(self):
        try:
            min_t = float(self.filter_temp_entry.get())
            results = [i for i in self.history if i["temp"] > min_t]
            self.refresh_table(results)
        except ValueError:
            messagebox.showwarning("Внимание", "Введите число для фильтрации")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
