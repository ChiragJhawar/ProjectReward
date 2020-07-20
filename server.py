from flask import Flask, request, jsonify
from PRApurv import ProjectRewarder

worker = ProjectRewarder(None, None, None, None)

app = Flask(__name__)

'''
    ./ngrok http 7500
    curl -X POST -d "ticker=GOOG" localhost:7500/api/set_ticker
    curl -X POST -d "date=2020-08-21" localhost:7500/api/set_date
    curl -X POST -d "flag=calls" localhost:7500/api/set_flag
    curl -X POST -d "spread_type=credit" localhost:7500/api/set_type

'''

@app.route('/api/set_ticker', methods=['POST'])
def setTicker():
    #when passing in variables to a flask method, check request.args, request.form, and request.json
    response = worker.setTicker(request.form['ticker'])
    print(worker)
    return jsonify(response)

@app.route('/api/set_date', methods=['POST'])
def setDate():
	response = worker.setDate(request.form['date'])
	print(worker)
	return jsonify(response)
@app.route('/api/set_flag', methods=['POST'])
def setFlag():
	response = worker.setFlag(request.form['flag'])
	print(worker)
	return jsonify(response)
@app.route('/api/set_type', methods=['POST'])
def setType():
	response = worker.setType(request.form['spread_type'])
	print(worker)
	return jsonify(response)
@app.route('/api/spread/basic_spreads', methods=['GET'])
def getSpread():
	worker.getBasicSpread()
	return jsonify(worker.best_ratio)

app.run(debug=True, port=7500)
