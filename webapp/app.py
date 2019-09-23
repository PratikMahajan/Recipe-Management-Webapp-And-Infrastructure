from flask import Flask, Response, request, jsonify
import mysql.connector as mariadb
from config.loggingfilter import *

app = Flask(__name__)


# CREATE DATABASE

mariadb_conn = mariadb.connect(user='some_user', password='some_pass', database='user_list')
cur = mariadb_conn.cursor()
cur.execute("CREATE TABLE usr_tbl (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(50), firstname VARCHAR(50), lastname VARCHAR(50), emailaddress VARCHAR(50) );")
mariadb_conn.commit()
mariadb_conn.close()

# CREATE CONNECTION 
# CLOSE CONNECTION
# INITIALIZE THE DATABASE

#=====================================
# API ENDPOINTS
#====================================

# CREATE USER ACCOUNT
@app.route('/signUp', method=['POST'])
def signUp():
    fname = request.json['user_fname']
    lname = request.json['user_lname']
    emailaddress = request.json['user_emailaddress']
    passwrd = request.json['user_password']


@app.route('/health', methods=['GET', 'POST'])
@disable_logging
def health_probe() -> Response:
    status = dict()
    status["ok"] = True
    return Response(json.dumps(status), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
