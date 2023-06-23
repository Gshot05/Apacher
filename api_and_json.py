import requests
import json
import tkinter as tk
from tkinter import filedialog, messagebox

def get_all_ip_addresses():
    response = requests.get('http://127.0.0.1:5000/api/ip-addresses')
    if response.status_code == 200:
        data = response.json()
        path_to_save = filedialog.asksaveasfilename(defaultextension=".json")
        if path_to_save:
            try:
                with open(path_to_save, 'w') as file:
                    json.dump(data, file)
                messagebox.showinfo("Успех", f"Данные успешно сохранены в {path_to_save}!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении данных: {str(e)}")
        else:
            messagebox.showinfo("Информация", "Операция отменена.")
    else:
        messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {response.status_code}")

def open_date_range_form():
    date_range_form = tk.Toplevel(root)
    date_range_form.title("Выбор дат")
    date_range_form.configure(bg="black")

    start_date_label = tk.Label(date_range_form, text="Начальная дата (ГГГГ-ММ-ДД):", fg="white", bg="black")
    start_date_label.pack()
    start_date_entry = tk.Entry(date_range_form)
    start_date_entry.pack()

    end_date_label = tk.Label(date_range_form, text="Конечная дата (необязательно):", fg="white", bg="black")
    end_date_label.pack()
    end_date_entry = tk.Entry(date_range_form)
    end_date_entry.pack()

    save_button = tk.Button(date_range_form, text="Сохранить", command=lambda: get_dates_in_range(date_range_form, start_date_entry.get(), end_date_entry.get()), bg="black", fg="white")
    save_button.pack()

    # Изменение фона элементов формы
    date_range_form.configure(bg="black")
    start_date_entry.configure(bg="white", fg="black")
    end_date_entry.configure(bg="white", fg="black")
    save_button.configure(bg="black", fg="white")

def get_dates_in_range(date_range_form, start_date, end_date):
    date_range_form.destroy()

    file_path = filedialog.asksaveasfilename(defaultextension=".json")

    url = 'http://127.0.0.1:5000/api/dates?start_date=' + start_date

    if end_date:
        url += '&end_date=' + end_date

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    json.dump(data, file)
                messagebox.showinfo("Успех", "Данные успешно сохранены в файл: " + file_path)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении данных: {str(e)}")
        else:
            messagebox.showinfo("Информация", "Операция отменена.")
    else:
        messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {response.status_code}")

def exit_program():
    root.destroy()

# Создание главного окна
root = tk.Tk()
root.title("Управление данными")
root.configure(bg="black")

# Создание виджетов
label = tk.Label(root, text="Выберите действие:", fg="white", bg="black")
label.pack()

button1 = tk.Button(root, text="Получить все IP-адреса и сохранить в файл", command=get_all_ip_addresses, bg="black", fg="white")
button1.pack()

button2 = tk.Button(root, text="Получить даты в заданном временном промежутке и сохранить в файл", command=open_date_range_form, bg="black", fg="white")
button2.pack()

button3 = tk.Button(root, text="Выход", command=exit_program, bg="black", fg="white")
button3.pack()

# Запуск основного цикла обработки событий
root.mainloop()
