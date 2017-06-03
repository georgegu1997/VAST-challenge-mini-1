import json
from datetime import datetime, timedelta

epoch = datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Record:
    def __init__(self, time, position):
        self.time = time
        self.position = position

class Travel:
    #static property of all travel instances
    all_travels = []
    def __init__(self, car_id, car_type):
        self.id = car_id
        self.type = car_type
        self.records = []
        Travel.all_travels.append(self)

    @staticmethod
    def static_find_by_id(car_id):
        for travel in Travel.all_travels:
            if travel.id == car_id:
                return travel
        return None

    @staticmethod
    def static_print_all():
        for travel in Travel.all_travels:
            travel.printSelf()

    @staticmethod
    def get_type_by_number(number):
        if number == "1":
            return "2 axle car (or motoecycle)"
        elif number == "2":
            return "2 axle truck (without pass)"
        elif number == "3":
            return "3 axle truck"
        elif number == "4":
            return "4 axle (and above) truck"
        elif number == "5":
            return "2 axle bus"
        elif number == "6":
            return "3 axle bus"
        else:
            return "2 axle truck (with Pass)"

    @staticmethod
    def get_jsonable_all():
        travels = []
        for travel in Travel.all_travels:
            travel_json = travel.get_jsonable()
            travels.append(travel_json)
        return travels

    def get_jsonable(self):
        travel = self
        travel_json = {
        'car_id': travel.id,
        'car_type': travel.type,
        'records': []
        }
        for record in travel.records:
            travel_json['records'].append({
            'gate_name': record.position,
            'timestamp': unix_time_millis(record.time)
            })
        return travel_json

    def add_record(self, record):
        self.records.append(record)

    def printSelf(self):
        print self.id
        print self.type
        for record in self.records:
            print record.time,record.position,"->",
        print ""

    def get_type_str(self):
        if self.type == "1":
            return "2 axle car (or motoecycle)"
        elif self.type == "2":
            return "2 axle truck (without pass)"
        elif self.type == "3":
            return "3 axle truck"
        elif self.type == "4":
            return "4 axle (and above) truck"
        elif self.type == "5":
            return "2 axle bus"
        elif self.type == "6":
            return "3 axle bus"
        else:
            return "2 axle truck (with Pass)"

    def same_route(self, travel):
        if len(self.records) != len(travel.records):
            return False
        for i in range(len(self.records)):
            if self.records[i].position != travel.records[i].position:
                return False
        return True

    def get_total_time(self):
        entry_time = self.records[0].time
        exit_time = self.records[-1].time
        time_spent = exit_time - entry_time
        return time_spent

    def get_entry_time(self):
        return self.records[0].time

class Route:
    all_routes = []

    def __init__(self, travel = None):
        if travel != None:
            self.records = travel.records
        else:
            self.records = []
        self.travels = []
        Route.all_routes.append(self)
        self.type_count = {
        "1":0,
        "2":0,
        "2P":0,
        "3":0,
        "4":0,
        "5":0,
        "6":0
        }

    @staticmethod
    def find_by_records(records):
        for route in Route.all_routes:
            if route.has_same_records(records):
                return route
        return None

    @staticmethod
    def add_or_update(travel):
        route = Route.find_by_records(travel.records)
        if route == None:
            route = Route(travel)
        route.add_travel(travel)

    @staticmethod
    def print_all(type = False):
        for route in Route.all_routes:
            for i in range(len(route.records)):
                print route.records[i].position,
                if i != len(route.records) - 1:
                    print "->",
                else:
                    print ""
            if type == False:
                print "Total count:", len(route.travels)
            else:
                print "Total count:", len(route.travels)
                for k,v in route.type_count.items():
                    print Travel.get_type_by_number(k)+": "+str(v)
            print ""
        print ""
        print "Total Routes: "+ str(len(Route.all_routes))

    @staticmethod
    def sort_by_frequency():
        Route.all_routes.sort(key=lambda x: len(x.travels), reverse = True)

    @staticmethod
    def get_jsonable_all():
        routes = []
        for route in Route.all_routes:
            routes.append(route.get_jsonable())
        return routes

    def get_jsonable(self):
        route_json = {
        "records": [],
        "type_count": self.type_count,
        "total_count": len(self.travels),
        "travels": []
        }
        for record in self.travels[0].records:
            route_json["records"].append(record.position)
        for travel in self.travels:
            route_json["travels"].append(travel.get_jsonable())
        return route_json

    def add_travel(self, travel):
        self.travels.append(travel)
        self.type_count[travel.type] += 1

    def has_same_records(self, records):
        if len(self.records) != len(records):
            return False
        for i in range(len(self.records)):
            if self.records[i].position != records[i].position:
                return False
        return True
