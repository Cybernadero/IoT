  
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api
from sensors import Sensors

import db_config as database


app=Flask(__name__)
api=Api(app)
CORS(app)

@app.route("/createGreenhouse/", methods=['GET'])
def createGreenhouse():

    IdArduino = request.args.get("IdArduino")
    flag = Sensors.check_if_arduino_exists(IdArduino)
    print(flag)
    if(flag):
        date = request.args.get("date")
        response = str(database.db.sensors.insert_one(
                {
                    'IdArduino':IdArduino,
                    'temperature':0,
                    'humidity':0,
                    'lastStatus':date,
                    'measurements':[]
                }
            ).inserted_id)

    if flag:
        return jsonify({"response":response, "IdArduino":IdArduino, "date":date})
    else:
        return jsonify({'message':'Arduino already exists'})


@app.route("/insertData/", methods=['GET'])
def insert():
    IdArduino = request.args.get("IdArduino")
    temperature = request.args.get("temperature")
    humidity = request.args.get("humidity")
    date = request.args.get("date")

    database.db.sensors.update_one({'IdArduino':IdArduino},
        {
            '$push':{
            'measurements':{
                'temperature':temperature,
                'humidity':humidity,
                'date':date
            }},
            '$set':{
            'temperature':temperature,
            'humidity':humidity,
            'date':date,
            'lastUpdate':date,
            }
        })

    return jsonify({"IdArduino":IdArduino,"temperature":temperature,"humidity":humidity, "date":date})

api.add_resource(Sensors, '/delete/')    

if __name__ == '__main__':
    app.run(load_dotenv=True)