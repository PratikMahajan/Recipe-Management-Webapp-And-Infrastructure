from flask import Flask, Response, request, jsonify
#import mysql.connector as mariadb
from config.loggingfilter import *
from config.envvar import *


# CONNECTION TO MARIADB

mariadb_conn = mariadb.connect(user=config.db_config["DB_USER"], password= config.db_config["DB_PASSWORD"]) 
database =config.db_config["DB_NAME"]

cur = mariadb_conn.cursor()

mariadb_conn.commit()
mariadb_conn.close()
    


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
    res = cur.execute("Select id, first_name, last_name, email from user_info")
    for row in res:
        items = {}
        items['id'] = str(row[0])
        items['first_name'] = str(row[1])
        items['last name'] = str(row[2])
        items['email'] = str(row[3])
        return Response(json.dumps(status), status=200, mimetype='application/json')


