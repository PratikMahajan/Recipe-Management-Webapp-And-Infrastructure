from flask import Flask, Response, request, jsonify
#import mysql.connector as mariadb
from config.loggingfilter import *
from config.envvar import *


# CONNECTION TO MARIADB

def get_db():
    mariadb_connection = mariadb.connect(user=config.db_config["DB_USER"], password= config.db_config["DB_PASSWORD"], database =config.db_config["DB_NAME"])
    return mariadb_connection

#cur = mariadb_conn.cursor()

#mariadb_conn.commit()
#mariadb_conn.close()
    


@app.route('/health', methods=['GET', 'POST'])
@disable_logging
def health() -> Response:
    status = dict()
    status["ok"] = True
    return Response(json.dumps(status), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)



#===================================================================
# API ENDPOINTS
#===================================================================

@app.route('getacc', methods=['POST'])
def getacc():
    cur = get_db().cursor()
    res = cur.execute("Select id, first_name, last_name, email, password, account_created, account_updated from user_info")
    for row in res:
        items = {}
        items['id'] = str(row[0])
        items['first_name'] = str(row[1])
        items['last name'] = str(row[2])
        items['email'] = str(row[3])
        items['password'] = str(row[4])
        items['account_created'] = str(row[5])
        items['account_updated'] = str(row[5])

        return Response(json.dumps(status), status=200, mimetype='application/json')
    return Response(status=400)


@app.route("/CreateAccount", methods =['POST'])
def CreateAccount():
    try:
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        email = request.json['email']
        password = request.json['password']
        cur = get_db().cursor()
        checkUsername = cur.execute("Select user_id from user_info where email=? Limit 1", (email))
        if checkUsername.fetchall():
            response={}
            response["error"] = "Username already exists !!!!!"
            return Response(json.dumps(response), status=400, mimetype='application/json')


        res = cur.execute("INSERT into user_info (first_name, last_name, email, password) values(?,?,?,?,?);", (first_name, last_name, email, password))
        get_db().commit()
        return Response(status=200)
    except Exception as e:
        get_db().rollback()
        print(e)
        return Response(status=403)


@app.route("/UserLogin", methods=['POST'])
def UserLogin():
    try:
        email = request.json['email']
        password = request.json['password']
        cur = get_db().cursor()
        checkUsername = cur.execute("Select email, password from user_profile where email=? Limit 1", (email,)).fetchall()
        if not checkUsername:
            response={}
            response["error"] = "Username doesnt exists !!!!!"
            return Response(json.dumps(response), status=406, mimetype='application/json')
        savedPass = checkUsername[0][1]
        if savedPass = password:
            return Response(status = 200)
        else:
            response = {}
            respose["error"] = "Incorrect Password"
            return Response(json.dumps(response), status=406, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(status=400)


