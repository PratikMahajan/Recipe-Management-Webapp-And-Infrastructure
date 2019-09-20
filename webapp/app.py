from flask import Flask, Response
from config.loggingfilter import *

app = Flask(__name__)

@app.route('/health', methods=['GET', 'POST'])
@disable_logging
def health_probe() -> Response:
    status = dict()
    status["ok"] = True
    return Response(json.dumps(status), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)