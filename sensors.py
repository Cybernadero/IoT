from flask import Flask, json, jsonify, request
from flask_restful import Resource, abort
from flask_pymongo import pymongo
from bson.json_util import ObjectId
import db_config as database


class Sensors(Resource):
   
    def get(self, by, data):
        response = self.abort_if_not_exist(by, data)
        response['_id'] = str(response['_id'])
        return jsonify(response)

    def post(self):
        _id = str(database.db.sensors.insert_one({
            'IdSensor':request.json['IdSensor'],
            'SensorValue':request.json['SensorValue'],
        }).inserted_id)
        return jsonify({"_id":_id})


    def abort_if_not_exist(self,by,data):
        if by == "_id":
            response = database.db.sensors.find_one({"_id":ObjectId(data)})
        else:
            response = database.db.sensors.find_one({f"{by}": data})
            
        if response:
            return response
        else:
            abort(jsonify({"status":404, f"{by}":f"{data} not found"}))