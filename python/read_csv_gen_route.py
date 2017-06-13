'''
For VAST Challenge 2017 Mini Challenge 1
Author: GU Qiao, George @ HKUST
E-mail: georgegu1997@gmail.com

This script reads the csv file given by the challenge, generate the travels and
routes of from the records. and can print them or write them into a json file
'''

import csv
import json
from datetime import datetime

from classes import *

def read_travels():
    with open("Lekagul Sensor Data.csv","rb") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",",quotechar="|")
        i = 0
        for row in spamreader:
            #ignore the title of the table
            i += 1
            if i == 1:
                continue
            if i > 1000:
                break
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
    generate_route()
    Route.sort_by_frequency()

    #print Travel.get_jsonable()
    #generate_route()
    #Route.sort_by_frequency()
    Route.print_all(True);
    #cal_all_records()

if __name__ == "__main__":
    main()
