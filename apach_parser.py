from ua_parser import user_agent_parser

def parse_logs(log_path, conn):
    # Открываем файл с логами
    with open(log_path, 'r') as f:
        for line in f:
            # Разбираем строку лога
            log_parts = line.split()

            # Проверяем, что количество частей лога достаточно
            if len(log_parts) < 10:
                # Лог не содержит всех необходимых данных, пропускаем его
                continue

            try:
                # Извлекаем нужные данные
                ip_address = log_parts[0]
                date = log_parts[3].strip('[]')
                request_method = log_parts[5].strip('"')
                url = log_parts[6]
                http_version = log_parts[7].split('/')[1].strip()# Удаляем лишние пробелы
                status_code = int(log_parts[8])
                response_size = int(log_parts[9])

                # Сохраняем данные в БД
                cur = conn.cursor()
                cur.execute("INSERT INTO access_logs (ip_address, date, request_method, url, http_version, status_code, response_size) VALUES (%s, %s, %s, %s, %s, %s, %s)", (ip_address, date, request_method, url, http_version, status_code, response_size))
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
