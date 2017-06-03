import json, csv
from pprint import pprint
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import matplotlib.dates as mdates

from PIL import Image
import numpy as np

from classes import *
from punchcard import *

def read_json(file_name):
    with open(file_name) as data_file:
        data = json.load(data_file)
    return data

def restore_route_instance(route_dict):
    route = Route()
    route.type_count = route_dict['type_count']
    for travel_dict in route_dict['travels']:
        travel = Travel(travel_dict['car_id'], travel_dict['car_type'])
        for record_dict in travel_dict['records']:
            time = datetime(1970, 1, 1) + timedelta(milliseconds=int(record_dict['timestamp']))
            record = Record(time,record_dict['gate_name'])
            travel.records.append(record)
        route.travels.append(travel)
        if len(route.records) <= 0:
            route.records = travel.records

def restore_data(data):
    for route_dict in data:
        restore_route_instance(route_dict)

def read_positions():
    gate_positions = {}
    with open("sensor_position.csv", "rb") as csvfile:
        spamreader = csv.reader(csvfile, delimiter="\t",quotechar="|")
        i = 0
        for row in spamreader:
            i += 1
            if i == 1:
                continue
            gate_name = row[0]
            gate_x = int(row[1])
            gate_y = int(row[2])
            gate_positions[gate_name] = {'x': gate_x, 'y': gate_y}
    return gate_positions

def draw_route(points, ax):
    im = plt.imread("Lekagul_Roadways.png")
    ax.imshow(im)
    if len(points) != 0:
        for i in range(0, len(points)-1):
            current_point = points[i]
            next_point = points[i+1]
            dx = next_point['x'] - current_point['x']
            dy = next_point['y'] - current_point['y']
            arrow = patches.Arrow(current_point['x'], current_point['y'], dx, dy, linewidth=1, edgecolor='r')
            ax.add_patch(arrow)
    return

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

def draw_distribution_plot(route, ax):
    data = []
    for travel in route.travels:
        data.append(travel.get_entry_time())

    # convert the epoch format to matplotlib date format
    # mpl_data = mdates.epoch2num(data)

    # plot it
    ax.hist(data, bins=50, color='lightblue')
    locator = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
    ax.set_title("Histogram for Entry Time")
    return

def draw_stayting_time_plot(route, ax):
    data = []
    for travel in route.travels:
        data.append(travel.get_total_time().total_seconds() * 1.0)
    max_staying_time = max(data)

    # convert the epoch format to matplotlib date format
    mpl_data = mdates.epoch2num(data)

    # plot it
    ax.hist(mpl_data, bins=30, color='lightgreen')
    if max_staying_time < 5*60*60:
        locator = mdates.MinuteLocator()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.set_title("Histogram for Staying Time(in hour and minute)")
    elif max_staying_time < 20*24*60*60:
        locator = mdates.HourLocator()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%dd%H'))
        ax.set_title("Histogram for Staying Time(in day and hour)")
    else:
        locator = mdates.DayLocator()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%mm%d'))
        ax.set_title("Histogram for Staying Time(in month and day)")
    ax.xaxis.set_minor_locator(locator)
    ax.xaxis.set_major_locator(plt.MaxNLocator(8))
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
    draw_distribution_plot(route, p3)
    draw_stayting_time_plot(route, p4)
    plt.figure()
    draw_punchcard_plot(route)
    #plt.show()

def flip_y(gate_positions):
    for k, v in gate_positions.items():
        v['y'] = 200 - v['y']
    return gate_positions

def main():
    routes_data = read_json('routes.json')
    restore_data(routes_data)
    gate_positions = read_positions()
    gate_positions = flip_y(gate_positions)
    handle_route(Route.all_routes[0], gate_positions)
    #plt.show()
    for i in range(50):
        handle_route(Route.all_routes[i], gate_positions)
        save_name = "./plot/"+ str(i) + "_1.png"
        plt.savefig(save_name)
        plt.close()
        save_name = "./plot/"+ str(i) + "_2.png"
        plt.savefig(save_name)
        plt.close('all')

if __name__ == "__main__":
    main()
