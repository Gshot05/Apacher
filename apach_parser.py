from datetime import datetime

def parse_logs(log_path, conn):
    # Открываем файл с логами
    with open(log_path, 'r') as f:
        for line in f:
            # Разбираем строку лога
            log_parts = line.split('"')

            # Проверяем, что количество частей лога достаточно
            if len(log_parts) < 3:
                # Лог не содержит всех необходимых данных, пропускаем его
                continue

            try:
                # Извлекаем нужные данные
                log_info = log_parts[0].split()
                ip_address = log_info[0]
                date_str = log_info[3].lstrip('[')
                date = datetime.strptime(date_str, '%d/%b/%Y:%H:%M:%S')
                request_parts = log_parts[1].split()
                request_method = request_parts[0]
                url = request_parts[1]
                http_version = request_parts[2]
                status_code = int(log_parts[2].split()[0])
                response_size = int(log_parts[2].split()[1])

                # Сохраняем данные в БД
                cur = conn.cursor()
                cur.execute("INSERT INTO access_logs (ip_address, date, request_method, url, http_version, status_code, response_size) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (ip_address, date, request_method, url, http_version, status_code, response_size))
                conn.commit()
            except IndexError:
                # Ошибка индекса - формат записи лога неверен
                print("Ошибка индекса в строке лога:", line)
                continue
            except ValueError:
                # Ошибка преобразования типов - неверный формат числовых данных
                print("Ошибка преобразования типов в строке лога:", line)
                continue
            except Exception as e:
                # Обработка других исключений
                print("Ошибка при обработке строки лога:", str(e))
                continue

