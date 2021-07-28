from flask_restful import Resource

import db_config as database


class Sensors(Resource): 
    def delete(self):
        return database.db.sensors.delete_many({}).deleted_count

    def check_if_arduino_exists(data):
        response = database.db.sensors.find_one({'IdArduino':data})

        if response:
            return False
        else:
            return True