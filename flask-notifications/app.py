from flask import Flask, render_template, url_for, jsonify, request, json
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'gas_detection_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
MySQL = MySQL(app)
CORS(app)

#JSON body format { "device_id":"1", "gas":"Butane", "reading":"9999" }

@app.route('/post/notif', methods=['POST'])
def index():
    conn = MySQL.connection
    cursor = conn.cursor()

    if request.method == 'POST':
        device_id = request.json['device_id']
        gas = request.json['gas']
        reading = request.json['reading']
        
        cursor.execute('SELECT room FROM devices WHERE device_id = {}'.format(device_id))
        room = cursor.fetchone()['room']
        print(room)

        cursor.execute('INSERT INTO notifications(devices_device_id, room, gas, reading) VALUES({}, "{}", "{}", "{}")'.format(device_id, room, gas, reading))
        conn.commit()
    
    return "POST request success"


if __name__ == "__main__":
    app.run(debug = True)
    # app.run(debug = True, host= '192.168.43.90')