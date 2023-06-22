from flask import Flask, render_template, request, jsonify
import psycopg2
from apach_parser import parse_logs
import json
import requests

app = Flask(__name__)

# Подключаемся к БД
conn = psycopg2.connect(database="Apacher", user="rootuser", password="@p@ch3r", host="localhost")


@app.route('/upload', methods=['POST'])
def upload_file():
    log_path = request.form['log_path']
    
    parse_logs(log_path, conn)

    return "File uploaded successfully."


@app.route('/upload_form', methods=['GET'])
def show_upload_form():
    return render_template('upload_form.html')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/ip-addresses', methods=['GET'])
def view_all_ip_addresses():
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT ip_address FROM access_logs")
    rows = cur.fetchall()
    ip_addresses = [row[0] for row in rows]
    return render_template('ip_addresses.html', ip_addresses=ip_addresses)


@app.route('/dates', methods=['GET'])
def view_dates():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    cur = conn.cursor()

    try:
        if end_date:
            cur.execute("SELECT DISTINCT date FROM access_logs WHERE date BETWEEN %s AND %s", (start_date, end_date))
        else:
            cur.execute("SELECT DISTINCT date FROM access_logs WHERE date >= %s", (start_date,))

        rows = cur.fetchall()
        dates = [row[0] for row in rows]

        return render_template('dates.html', dates=dates)

    except Exception as e:
        return "An error occurred: {}".format(str(e))

    finally:
        cur.close()


@app.route('/api/ip-addresses', methods=['GET'])
def get_all_ip_addresses():
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT ip_address FROM access_logs")
    rows = cur.fetchall()
    ip_addresses = [row[0] for row in rows]

    return jsonify(ip_addresses)


@app.route('/api/dates', methods=['GET'])
def get_dates():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    cur = conn.cursor()

    try:
        if end_date:
            cur.execute("SELECT DISTINCT date FROM access_logs WHERE date BETWEEN %s AND %s", (start_date, end_date))
        else:
            cur.execute("SELECT DISTINCT date FROM access_logs WHERE date >= %s", (start_date,))

        rows = cur.fetchall()
        dates = [row[0] for row in rows]

        return jsonify(dates)

    except Exception as e:
        return jsonify(error=str(e))

    finally:
        cur.close()


@app.route('/view-all', methods=['GET'])
def view_all():
    cur = conn.cursor()
    cur.execute("SELECT * FROM access_logs")
    rows = cur.fetchall()

    # Создание списка словарей для хранения результатов
    data = []
    for row in rows:
        item = {
            'ip_address': row[1],
            'date': row[2],
            'request_method': row[3],
            'url': row[4],
            'http_version': row[5],
            'status_code': row[6],
            'response_size': row[7],
            # Добавьте другие поля, если есть
        }
        data.append(item)

    return render_template('view_all.html', records=data)


if __name__ == '__main__':
    app.run()