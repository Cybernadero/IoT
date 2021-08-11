from bson.objectid import ObjectId
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource, abort

import db_config as database


app=Flask(__name__)
api=Api(app)
CORS(app)


class Sensors(Resource): 
    
    def post(self):
        _id = str(database.db.sensors.insert_one({     
            'UserId':request.json['UserId'],
            'IdArduino':request.json['IdArduino'],
            'temperature':request.json['temperature'],
            'humidity':request.json['humidity'],
            'lastUpdate':request.json['lastUpdate'],
            'measurements':[]
            
        }).inserted_id)
    
        return jsonify({"_id":_id})
    
    def get(self, by, data):
        response = self.abort_if_not_exist(by, data)
        response['_id'] = str(response['_id'])
        return jsonify(response)
        
        
    def abort_if_not_exist(self,by,data):
        if by == "_id":
            response = database.db.sensors.find_one({"_id":ObjectId(data)})
        else:
            response = database.db.sensors.find_one({f"{by}": data})
            
        if response:
            return response
        else:
            abort(jsonify({"status":404, f"{by}":f"{data} not found"}))


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
            'lastUpdate':date,
            }
        }
    )
    return jsonify({"IdArduino":IdArduino,"temperature":temperature,"humidity":humidity, "date":date})

api.add_resource(Sensors, '/createGreenhouse/', '/<string:by>:<string:data>/')    

if __name__ == '__main__':

    app.run(load_dotenv=True)