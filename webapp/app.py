from flask import Flask, Response, request, jsonify
import mysql.connector as mariadb
from datetime import datetime
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




#===================================================================
# API ENDPOINTS
#===================================================================

@app.route('/v1/user', methods=['GET','POST', 'PUT'])
def v1/user():
    if request.method == 'POST':
        #CREATE NEW USER
        try:
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        email = request.json['email']
        password = request.json['password']
        account_created = datetime.now()
        account_updated = datetime.now()
        cur = get_db().cursor()
        checkUsername = cur.execute("Select email from user_info where email=? Limit 1", (email))
        if checkUsername.fetchall():
            response={}
            response["error"] = "Username already exists !!!!!"
            return Response(json.dumps(response), status=400, mimetype='application/json')


        res = cur.execute("INSERT into user_info (first_name, last_name, email, password, account_created, account_updated) values(?,?,?,?,?,?,?);", (first_name, last_name, email, password, account_created, account_updated))
        get_db().commit()
        return Response(status=201)
    except Exception as e:
        get_db().rollback()
        print(e)
        return Response(status=400)

    if request.method == 'GET':
        #GET USER HERE
        try:
            email = request.json['email']
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
                items['account_updated'] = str(row[6])
                return Response(json.dumps(status), status=200, mimetype='application/json')
            return Response(status=401)
        except Exception as e:
            print(e)
            return Response(status=400)

    if request.method == 'PUT':
        #UPDATE USER
        try:
            #UPDATE PASSWORD
            try:
                email = request.json['email']
                oldPassword = request.json['oldpassword']
                newPassword = request.json['newpassword']
                cur = get_db().cursor()
                checkUsername = cur.execute("Select email, password from user_profile where email=? Limit 1", (email,)).fetchall()
                if not checkUsername:
                    response = {}
                    response["error"] = "Username not found"
                    return Response(json.dumps(response), status=400, mimetype='application/json')
                savedPass == checkUsername[0][1]
                if savedPass == oldPassword:
                    cur.execute("UPDATE user_profile SET password =? where username=?", (newPassword, email,))
                    get_db().commit()
                    return Response(status=200)
                else:
                    response = {}
                    response["error"] = "Incorrect Password !!!!!"
                    return Response(json.dumps(response), status=400, mimetype='application/json')
            execpt Exception as e:
                get_db().rollback()
                print(e)
                return Response(status=400)

            #UPDATE FIRST NAME
            #UPDATE LAST NAME
            try:
                email = request.json['email']
                first_name = request.json['first_name']
                last_name = request.json['last_name']
                cur = get_db().cursor()
                checkUser = cur.execute("Select email from user_profile where email=? Limit 1", (email,)).fetchall()
                if not checkUser:
                    response = {}
                    response["error"] = "User Not Found !!!!!"
                    return Response(json.dumps(response), status=400, mimetype='application/json')

                cur.execute("UPDATE user_profile SET first_name=?, last_name=? where email=?",(first_name, last_name, email))
                get_db().commit()
                return Response(status=200)
            except Exception as e:
                get_db().rollback()
                print(e)
                return Response(status=400)

        except Exception as e:
            get_db().rollback()
            print(e)
            return Response(status=401)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

