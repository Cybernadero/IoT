from flask import Flask, jsonify, request
from flask_restful import Api
from flask_cors import CORS
from sensors import Sensors
import db_config as database

app=Flask(__name__)
api=Api(app)
CORS(app)


@app.route('/option/', methods=["GET"])
def option():
    IdSensor = request.args.get("IdSensor")
    SensorValue = request.args.get("SensorValue")
    return jsonify({"IdSensor": IdSensor, "SensorValue": SensorValue})



api.add_resource(Sensors, '/new/','/<string:by>:<string:data>/')    

if __name__ == '__main__':
    app.run(load_dotenv=True)