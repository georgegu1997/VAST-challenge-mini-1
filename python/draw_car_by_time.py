import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Slider

from datetime import datetime, timedelta

from classes import *
from read_map_find_road import *

START_TIME = datetime(year=2015, month=5, day=1)
END_TIME = datetime(year=2016, month=5, day=31)

TOTAL_DAYS = int((END_TIME - START_TIME).total_seconds()/3600/24)
TOTAL_MINUTES_A_DAY = 24 * 60

'''configure the and define the global variable'''
plt.figure(figsize=(10,10))
ax_main = plt.axes([0.2,0.25,0.6,0.6])
ax_main.set_xlim(left = 0, right = 200)
ax_main.set_ylim(bottom = 0, top = 200)

axcolor = 'lightgoldenrodyellow'
ax_time = plt.axes([0.1, 0.1, 0.75, 0.03], facecolor=axcolor)
ax_date = plt.axes([0.1, 0.15, 0.75, 0.03], facecolor=axcolor)

sdate = Slider(ax_date, 'Date', 1, TOTAL_DAYS, valinit=1, dragging=True)
stime = Slider(ax_time, 'Time', 1, TOTAL_MINUTES_A_DAY, valinit=1, dragging=True)

map_analysis = MapAnalysis()

road_x = [x[0] for x in map_analysis.roads]
road_y = [x[1] for x in map_analysis.roads]
ax_main.scatter(road_x, road_y, color = "lightblue", alpha = 0.3)

car_plot, = ax_main.plot([], [], 'ro')

type_color_dict = {
    "1": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "2P": 6
}

def draw_road_on_main():
    for point in map_analysis.roads:
        rect = patches.Rectangle(
            (point[0], point[1]),
            width=1,
            height=1,
            color="lightblue",
            alpha=0.3)
        ax_main.add_patch(rect)
    return

def get_position_of_car(travel, time):
    assert(travel.get_entry_time() <= time)
    assert(travel.get_exit_time() >= time)
    for i in range(len(travel.records)):
        if travel.records[i].time > time:
            break
    next_record = travel.records[i]
    last_record = travel.records[i-1]
    rate = (time - last_record.time).total_seconds() * 1.0 / (next_record.time - last_record.time).total_seconds() * 1.0
    route_points = map_analysis.get_route_points(last_record.position, next_record.position)
    position = route_points[int(rate * len(route_points))]
    return position

def draw_car_on_main(time):
    travels = [x for x in Travel.all_travels if x.get_entry_time() < time and x.get_exit_time() > time]
    print "total car:", len(travels)
    px = []
    py = []
    pc = []
    for travel in travels:
        point = get_position_of_car(travel, time)
        px.append(point[0])
        py.append(point[1])
        pc.append(type_color_dict[travel.type])
    car_plot.set_data(px, py)
    return

def update_slider(val):
    '''make it discrete manually'''
    date_val = int(sdate.val)
    time_val = int(stime.val)
    dt = START_TIME + timedelta(days = date_val) + timedelta(minutes = time_val)
    draw_car_on_main(dt)
    print dt

def main():
    routes_data, gate_positions = read_all_data()
    #draw_road_on_main()

    sdate.on_changed(update_slider)
    stime.on_changed(update_slider)
    plt.show()



if __name__ == "__main__":
    main()
