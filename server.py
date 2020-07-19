from flask import Flask, request, jsonify
from PRaj import ProjectRewarder

worker = ProjectRewarder(None, None, None, None)

app = Flask(__name__)

'''
    curl -X POST -d "ticker=GOOG" localhost:7500/api/set_ticker
'''

@app.route('/api/set_ticker', methods=['POST'])
def setTicker():
    #when passing in variables to a flask method, check request.args, request.form, and request.json
    response = worker.setTicker(request.form['ticker'])
    print(worker)
    return jsonify(response)

app.run(debug=True, port=7500)
