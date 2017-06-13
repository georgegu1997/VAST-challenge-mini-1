'''
For VAST Challenge 2017 Mini Challenge 1
Author: GU Qiao, George @ HKUST
E-mail: georgegu1997@gmail.com

This script will plot all the different route of travels, the output will contain
5 parts: the route depicted by arrow on the real map; the car type distribution;
the distribution of entry times of the travels; the distribution of the lasting time
of the travels; and the punchcard of the entry times.
'''

import json, csv, re
from pprint import pprint
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import matplotlib.dates as mdates
from collections import Counter

from PIL import Image
import numpy as np

from classes import *
from punchcard import *


def get_type_str(type):
    if type == "1":
        return "2 axle car (or motorcycle)"
    elif type == "2":
        return "2 axle truck (without pass)"
    elif type == "3":
        return "3 axle truck"
    elif type == "4":
        return "4 axle (and above) truck"
    elif type == "5":
        return "2 axle bus"
    elif type == "6":
        return "3 axle bus"
    else:
        return "2 axle truck (with Pass)"

def draw_route_read_map(ax):
    im = plt.imread("Lekagul_Roadways.png")
    ax.imshow(im)

def draw_route_draw_arrows(points, ax):
    if len(points) != 0:
        for i in range(0, len(points)-1):
            current_point = points[i]
            next_point = points[i+1]
            dx = next_point['x'] - current_point['x']
            dy = next_point['y'] - current_point['y']
            arrow = patches.FancyArrow(
                current_point['x'], current_point['y'], dx, dy,
                linewidth=1,
                head_width=5,
                facecolor='r',
                edgecolor = 'r'
            )
            ax.add_patch(arrow)

def draw_route(points, ax):
    draw_route_read_map(ax)
    draw_route_draw_arrows(points, ax)
    '''
    im = plt.imread("Lekagul_Roadways.png")
    ax.imshow(im)
    if len(points) != 0:
        for i in range(0, len(points)-1):
            current_point = points[i]
            next_point = points[i+1]
            dx = next_point['x'] - current_point['x']
            dy = next_point['y'] - current_point['y']
            arrow = patches.FancyArrow(
                current_point['x'], current_point['y'], dx, dy,
                linewidth=1,
                head_width=5,
                facecolor='r',
                edgecolor = 'r'
            )
            ax.add_patch(arrow)
    '''

def draw_routes(points_arrs, ax):
    draw_route_read_map(ax)
    for points in points_arr:
        draw_route_draw_arrows(points, ax)

def draw_car_type_frequency(type_count, ax):
    x = range(3)
    tick_labels = ["car", "truck", "bus"]
    # 2 axles
    layer1 = np.array([type_count["1"], type_count["2"], type_count["5"]])
    # 2 axles with pass
    layer2 = np.array([0, type_count["2P"], 0])
    # 3 axles
    layer3 = np.array([0, type_count["3"], type_count["6"]])
    # 4 axles or above
    layer4 = np.array([0, type_count["4"], 0])
    ax.bar(x, layer1, label="2 axles")
    ax.bar(x, layer2, bottom=layer1, label="2 axles with pass")
    ax.bar(x, layer3, bottom=layer1+layer2, label="3 axles")
    ax.bar(x, layer4, bottom=layer1+layer2+layer3, label="4 axles or above", tick_label = tick_labels)
    ax.legend()

def gen_type_count_dict():
    list = {
    "1":  [],
    "2":  [],
    "2P": [],
    "3":  [],
    "4":  [],
    "5":  [],
    "6":  []
    }

    return list

def sort_entry_time_by_type(travels):
    sorted_list = gen_type_count_dict()
    max_date = min_date = travels[0].get_entry_time()
    for travel in travels:
        entry_time = travel.get_entry_time()
        if entry_time > max_date:
            max_date = entry_time
        if entry_time < min_date:
            min_date = entry_time
        sorted_list[travel.type].append(entry_time)
    date_intervel = max_date - min_date
    return sorted_list, date_intervel

def sort_staying_time_by_type(travels):
    sorted_list = gen_type_count_dict()
    max_time = travels[0].get_total_time().total_seconds() * 1.0
    for travel in travels:
        staying_time = travel.get_total_time().total_seconds() * 1.0
        if staying_time > max_time:
            max_time = staying_time
        sorted_list[travel.type].append(staying_time)
    return sorted_list, max_time

def draw_distribution_plot(travels, ax):
    '''
    data = []
    for travel in route.travels:
        data.append(travel.get_entry_time())
    max_date = max(data)
    min_date = min(data)
    date_intervel = max_date - min_date
    '''
    sorted_dict, date_intervel = sort_entry_time_by_type(travels)

    # plot it
    if len(travels) == 1:
        ax.set_title("Only Single Entry at "+max_date.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        for k, v in sorted_dict.items():
            if len(v) > 0:
                ax.hist(v, bins=80, alpha = 0.3, label = get_type_str(k))
        ax.legend()
        ax.xaxis.set_major_locator(plt.MaxNLocator(5))
        if date_intervel.total_seconds() < 3*60*60:
            locator = mdates.MinuteLocator()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H:%M'))
            ax.xaxis.set_major_locator(plt.MaxNLocator(3))
        elif date_intervel.total_seconds() < 24*60*60:
            locator = mdates.HourLocator()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H'))
            ax.xaxis.set_major_locator(plt.MaxNLocator(4))
        elif date_intervel.total_seconds() < 2*30*24*60*60:
            locator = mdates.DayLocator()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
        else:
            locator = mdates.MonthLocator()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))

        locator.MAXTICKS = 10000
        ax.xaxis.set_minor_locator(locator)

        ax.set_title("Histogram for Entry Time")
    return

def draw_stayting_time_plot(travels, ax):
    '''
    data = []
    for travel in route.travels:
        data.append(travel.get_total_time().total_seconds() * 1.0)
    max_staying_time = max(data)
    '''
    sorted_dict, max_staying_time = sort_staying_time_by_type(travels)
    max_staying_time = mdates.epoch2num(max_staying_time)

    # plot it
    if len(travels) == 1:
        ax.set_title("Only Single Entry lasting for: " + str(timedelta(seconds = max_staying_time)))
    else:
        for k, v in sorted_dict.items():
            # convert the epoch format to matplotlib date format
            v = mdates.epoch2num(v)
            if len(v) > 0:
                ax.hist(v, bins=80, alpha = 0.3, label = get_type_str(k))
        ax.legend()
        if max_staying_time < 5*60*60:
            locator = mdates.MinuteLocator()
        elif max_staying_time < 20*24*60*60:
            locator = mdates.HourLocator()
        elif max_staying_time < 3*30*24*60*60:
            locator = mdates.DayLocator()
        else:
            locator = mdates.MonthLocator()
        locator.MAXTICKS = 10000

        if max_staying_time < 24*60*60:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            ax.set_title("Histogram for Staying Time(in hour and minute)")
        elif max_staying_time < 30*24*60*60:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%dd%H'))
            ax.set_title("Histogram for Staying Time(in day and hour)")
        else:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%mm%d'))
            ax.set_title("Histogram for Staying Time(in month and day)")

        ax.xaxis.set_minor_locator(locator)
        ax.xaxis.set_major_locator(plt.MaxNLocator(6))
    return

def draw_punchcard_plot(route):
    infos = {}
    for d in range(7):
        for h in range(24):
            infos[(d, h)] = 0
    for travel in route.travels:
        start_time = travel.get_entry_time()
        dayofweek = start_time.weekday()
        hour = start_time.hour
        infos[(dayofweek, hour)] += 1
    draw_punchcard(infos)

def records2points(records, gate_positions):
    points = []
    for record in records:
        points.append(gate_positions[record.position])
    return points

def handle_route(route, gate_positions):
    plt.figure(figsize=(12, 10),dpi=120)
    p1 = plt.subplot(221)
    p2 = plt.subplot(222)
    p3 = plt.subplot(223)
    p4 = plt.subplot(224)
    points = records2points(route.records, gate_positions)
    '''
    for record in route.records:
        print "->",record.position,
    print ""
    print points
    '''
    draw_route(points, p1)
    draw_car_type_frequency(route.type_count, p2)
    draw_distribution_plot(route.travels, p3)
    draw_stayting_time_plot(route.travels, p4)
    plt.suptitle(route.return_records_for_print())
    if(len(route.travels) > 1):
        plt.figure()
        draw_punchcard_plot(route)

def handle_pattern(pattern, gate_positions):
    plt.figure(figsize=(12, 10),dpi=120)
    p1 = plt.subplot(221)
    p2 = plt.subplot(222)
    p3 = plt.subplot(223)
    p4 = plt.subplot(224)
    all_travels = []
    type_counter = Counter({
    "1":0,
    "2":0,
    "2P":0,
    "3":0,
    "4":0,
    "5":0,
    "6":0
    })
    for route in pattern:
        points = records2points(route.records, gate_positions)
        draw_route(points, p1)
        all_travels += route.travels
        type_counter += Counter(route.type_count)
    draw_car_type_frequency(type_counter, p2)
    draw_distribution_plot(all_travels, p3)
    draw_stayting_time_plot(all_travels, p4)



def get_important_records_of_route(route):
    camping = []
    entrance = []
    gate = []
    ranger_base = False
    for r in route.records:
        record = str(r.position)
        if re.match(r"camping", record):
            camping.append(record[-1])
        elif re.match(r"entrance", record):
            entrance.append(record[-1])
        elif re.match(r"ranger-base", record):
            ranger_base = True
        elif re.match(r"gate", record):
            gate.append(record[-1])
    return camping, entrance, gate, ranger_base

def gen_name(route):
    camping, entrance, gate, ranger_base = get_important_records_of_route(route)
    name = ""
    if ranger_base:
        name += "R_"
    if len(gate) > 0:
        name += "G"
        for i in gate:
            name += i
        name += "_"
    if len(camping) > 0:
        name += "C"
        for i in camping:
            name += i
        name += "_"
    if len(entrance) > 0:
        name += "E"
        for i in entrance:
            name += i
        name += "_"
    return name


def init_pattern_dict():
    patterns = {
        "camping": {
            "0":[],
            "1":[],
            "2":[],
            "3":[],
            "4":[],
            "5":[],
            "6":[],
            "7":[],
            "8":[],
            "multiple":[],
            "all": []
        },
        "ranger": []
    }
    return patterns

def sort_route_to_pattern(patterns, routes):
    print "sorting routes to patterns..."
    for i in range(len(routes)):
        route = routes[i]
        camping, entrance, gate, ranger_base = get_important_records_of_route(route)
        if ranger_base == True:
            patterns["ranger"].append(route)
        else:
            if len(camping) > 0:
                patterns["camping"]["all"].append(route)
            if len(camping) == 2:
                patterns["camping"][camping[0]].append(route)
            elif len(camping) > 2:
                patterns["camping"]["multiple"].append(route)
    print "done!"
    return patterns

def draw_all_route_and_save():
    routes_data, gate_positions = read_all_data()

    for i in range(len(Route.all_routes)):
        print i
        route = Route.all_routes[i]
        count = len(route.travels)
        handle_route(route, gate_positions)
        pre_fix = gen_name(route)
        if (len(route.travels) > 1):
            save_name = "./plot/routes/"+ pre_fix + str(count) + "_2.png"
            plt.savefig(save_name)
            plt.close()
        save_name = "./plot/routes/"+ pre_fix + str(count) + "_1.png"
        plt.savefig(save_name)
        plt.close('all')

def draw_first_route_and_show():
    routes_data, gate_positions = read_all_data()

    handle_route(Route.all_routes[0], gate_positions)
    plt.show()

def draw_patterns_and_save():
    routes_data, gate_positions = read_all_data()
    patterns = init_pattern_dict()
    patterns = sort_route_to_pattern(patterns, Route.all_routes)

    for number, routes in patterns["camping"].items():
        handle_pattern(routes, gate_positions)
        plt.suptitle("camping "+number)
        save_name = "./plot/patterns/"+"camping_"+number+".png"
        plt.savefig(save_name)
        plt.close('all')
        print "finished:", save_name

def main():
    draw_patterns_and_save()

if __name__ == "__main__":
    main()
