import requests
import json

while True:
    print("Выберите действие:")
    print("1. Получить все IP-адреса и сохранить в файл")
    print("2. Получить даты в заданном временном промежутке и сохранить в файл")
    print("3. Выход")

    choice = input("Введите номер действия: ")

    if choice == "1":
        path_to_save = input("Введите путь, куда вы хотите сохранить информацию: ")
        response = requests.get('http://127.0.0.1:5000/api/ip-addresses')
        if response.status_code == 200:
            data = response.json()
            try:
                with open(path_to_save, 'w') as file:
                    json.dump(data, file)
                print(f"Данные успешно сохранены в {path_to_save}!")
            except Exception as e:
                print("Ошибка при сохранении данных:", str(e))
        else:
            print('Ошибка при выполнении запроса:', response.status_code)

    elif choice == "2":
        start_date = input("Введите начальную дату в формате ГГГГ-ММ-ДД: ")
        end_date = input("Введите конечную дату в формате ГГГГ-ММ-ДД (необязательно): ")
        file_path = input("Введите путь для сохранения файла: ")

        url = 'http://127.0.0.1:5000/api/dates?start_date=' + start_date

        if end_date:
            url += '&end_date=' + end_date

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            try:
                with open(file_path, 'w') as file:
                    json.dump(data, file)
                print("Данные успешно сохранены в файл:", file_path)
            except Exception as e:
                print("Ошибка при сохранении данных:", str(e))
        else:
            print('Ошибка при выполнении запроса:', response.status_code)

    elif choice == "3":
        break

    else:
        print("Неверный выбор. Попробуйте снова.")
