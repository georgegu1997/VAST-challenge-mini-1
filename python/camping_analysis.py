import re

import numpy as np
import matplotlib.pyplot as plt

from classes import *
from plot_routes import get_important_records_of_route

def find_all_camping_route():
    camping_routes = []
    for route in Route.all_routes:
        camping, entrance, gate, ranger_base = get_important_records_of_route(route)
        if len(camping) == 2 and not ranger_base:
            camping_routes.append(route)
    return camping_routes

def get_travel_from_route(routes):
    travels =[]
    for route in routes:
        travels += route.travels
    return travels

def find_all_camping_travel():
    camping_routes = find_all_camping_route()
    return get_travel_from_route(camping_routes)

def sort_travels_by_type(travels):
    sorted_travels = {
        "0": []
    }
    for travel in travels:
        if travel.type in sorted_travels:
            sorted_travels[travel.type].append(travel)
        else:
            sorted_travels[travel.type] = [travel]
        sorted_travels["0"].append(travel)
    return sorted_travels

def sort_travels_by_camping_index(travels):
    sorted_travels = {
        "all":[]
    }
    for travel in travels:
        for record in travel.records:
            if re.match(r"camping", record.position):
                camping_position = record.position
                break
        if camping_position in sorted_travels:
            sorted_travels[camping_position].append(travel)
        else:
            sorted_travels[camping_position] = [travel]
        sorted_travels["all"].append(travel)

    for k, v in sorted_travels.items():
        print k, ":", len(v)
    return sorted_travels

def find_camping_travel_staying_time(travel):
    for i in range(len(travel.records) - 1):
        this_r = travel.records[i]
        next_r = travel.records[i+1]
        if re.match(r"camping", this_r.position) and re.match(r"camping", next_r.position):
            return next_r.time - this_r.time

'''The travels should be a list of travel which go to the designated camping area'''
def get_car_count_in_camping_by_time(travels, time):
    travels_in_preserve = [x for x in travels if x.get_entry_time() < time and x.get_exit_time() > time]
    counter = 0
    for travel in travels_in_preserve:
        for i in range(len(travel.records) - 1):
            this_r = travel.records[i]
            next_r = travel.records[i+1]
            if re.match(r"camping", this_r.position) and re.match(r"camping", next_r.position):
                if this_r.time < time and next_r.time > time:
                    counter += 1
                break
    return counter

def plot_camping_car_count(travels):
    time_offset = {
        "00:00":timedelta(hours=0),
        "06:00":timedelta(hours=6),
        "12:00":timedelta(hours=12),
        "18:00":timedelta(hours=18)
    }
    for k, v in time_offset.items():
        times = []
        counts = []
        time = START_TIME + v
        while time <= END_TIME:
            print time
            times = times + [time]
            time += timedelta(days=1)
            counts.append(get_car_count_in_camping_by_time(travels, time))
        plt.plot(times, counts, label=k)
    plt.xlabel("Time")
    plt.ylabel("Number of vehicles (all camping area)")
    plt.legend()

def plot_camping_car_count_by_type(sorted_travels):
    for k, v in sorted_travels.items():
        times = []
        counts = []
        time = START_TIME + timedelta(hours=18)
        while time <= END_TIME:
            print time
            times = times + [time]
            time += timedelta(days=1)
            counts.append(get_car_count_in_camping_by_time(v, time))
        plt.plot(times, counts, label=Travel.get_type_by_number(k))
    plt.xlabel("Time (At 18:00 of each day)")
    plt.ylabel("Number of vehicles (all camping area)")
    plt.legend()

def plot_camping_car_count_by_position(sorted_travels):
    for k, v in sorted_travels.items():
        times = []
        counts = []
        time = START_TIME + timedelta(hours=18)
        while time <= END_TIME:
            print time
            times = times + [time]
            time += timedelta(days=1)
            counts.append(get_car_count_in_camping_by_time(v, time))
        plt.plot(times, counts, label=k)
    plt.xlabel("Time (At 18:00 of each day)")
    plt.ylabel("Number of vehicles (all type)")
    plt.legend()

def plot_camping_staying_time_hist_by_type(travels, log = False):
    time_type_dict = {}
    for travel in travels:
        if travel.type in time_type_dict:
            time_type_dict[travel.type].append(find_camping_travel_staying_time(travel).total_seconds() / 3600.0)
        else:
            time_type_dict[travel.type] = [find_camping_travel_staying_time(travel).total_seconds() / 3600.0]
    for k, v in time_type_dict.items():
        plt.hist(v, bins=150, alpha = 0.3, label = Travel.get_type_by_number(k))
    plt.xlabel("staying time in camping area (in days and by type)")
    plt.ylabel("count")
    plt.xticks(range(0, 30*24, 24), range(0, 30))
    if log:
        plt.gca().set_yscale("log")
    plt.legend()

def plot_camping_staying_time_hist(travels, log = False):
    times = []
    for travel in travels:
        times.append(find_camping_travel_staying_time(travel).total_seconds() / 3600.0)
    plt.hist(times, bins = 300)
    plt.xlabel("staying time in camping area (in days)")
    plt.ylabel("count")
    if log:
        plt.gca().set_yscale("log")
    plt.xticks(range(0, 30*24, 24), range(0, 30))

def main():
    routes_data, gate_positions = read_all_data()
    camping_travels = find_all_camping_travel()
    type_sorted_travels = sort_travels_by_type(camping_travels)
    position_sorted_travels = sort_travels_by_camping_index(camping_travels)
    print len(camping_travels)
    #plot_camping_staying_time_hist_by_type(camping_travels, True)
    #plot_camping_car_count(camping_travels)
    #plot_camping_car_count_by_type(type_sorted_travels)
    plot_camping_car_count_by_position(position_sorted_travels)
    plt.show()

if __name__ == "__main__":
    main()
