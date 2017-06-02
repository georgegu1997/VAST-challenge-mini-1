import csv
import json
import io
from datetime import datetime

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
    def get_jsonable():
        travels = []
        travel_id = 1
        for travel in Travel.all_travels:
            travel_json = {
            'id':travel_id
            'car_id': travel.id,
            'car_type': travel.type,
            'records': []
            }
            for record in travel.records:
                travel_json['records'].append({
                'gate_name': record.position,
                'timestamp': unix_time_millis(record.time)
                })
            travels.append(travel_json)
            travel_id += 1
        return travels

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

    def get_total_time(self, travel):
        entry_time = self.records[0]
        exit_time = self.records[-1]
        time_spent = exit_time - entry_time
        return time_spent

class Route:
    all_routes = []

    def __init__(self, travel):
        self.records = travel.records
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
        Route.all_routes.sort(key=lambda x: len(x.travels))

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

def read_travels():
    with open("Lekagul Sensor Data.csv","rb") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",",quotechar="|")
        i = 0
        for row in spamreader:
            #ignore the title of the table
            i += 1
            if i == 1:
                continue
            """
            if i > 1000:
                break
            """
            dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            car_id = row[1]
            car_type = row[2]
            position = row[3]
            travel = Travel.static_find_by_id(car_id)
            if travel == None:
                travel = Travel(car_id,car_type)
            record = Record(dt, position)
            travel.add_record(record)

def generate_route():
    for travel in Travel.all_travels:
        Route.add_or_update(travel)

def cal_all_records():
    count = 0
    for route in Route.all_routes:
        record_count = len(route.records)
        travel_count = len(route.travels)
        count += record_count * travel_count
    print "Total record: " + str(count)

def write_in_json(data, file_name):
    with open(file_name, 'wb') as f:
        f.write(json.dumps(data, ensure_ascii=False))

def main():
    read_travels()
    #print Travel.get_jsonable()
    write_in_json(Travel.get_jsonable(), "travels.json")
    #generate_route()
    #Route.sort_by_frequency()
    #Route.print_all(True);
    #cal_all_records()

if __name__ == "__main__":
    main()
