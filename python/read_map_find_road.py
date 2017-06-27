'''
For VAST Challenge 2017 Mini Challenge 1
Author: GU Qiao, George @ HKUST
E-mail: georgegu1997@gmail.com

This script is used to analyze the map, it will read the map, find all the road points, and find the
road points between every two connected sensors.
'''

import csv, math, json
import numpy as np

from pprint import pprint
from scipy import misc

'''
SETUP:
    pip install scipy

FILE NEEDED:
    sensor_position.csv
    Lekagul Roadways.bmp

Please read the main() function as sample usage
'''

class MapAnalysis:

    def __init__(self):
        '''constant'''
        self.PICTURE_WIDTH = 200
        self.PICTURE_HEIGHT = 200

        '''A dict storing the position of all sensors on the map'''
        self.sensor_position = {}

        '''A numpy array storing the picture information'''
        self.image = np.array([])

        '''A list storing all the roads position (white pixel)'''
        self.roads = []

        '''A double dictionary storing the route from one sensor to another'''
        self.route_dict = {}

        '''Startup routine'''
        self.sensor_position = self.read_sensor_position()
        self.image = self.read_image()
        self.roads = self.get_all_road()
        self.route_dict = self.find_all_route()

    def read_sensor_position(self):
        sensor_positions = {}
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
                sensor_positions[gate_name] = {'x': gate_x, 'y': gate_y}
        return sensor_positions

    def read_image(self):
        image = misc.imread('Lekagul Roadways.bmp')
        return image

    def get_all_road(self):
        roads = []
        for r in range(self.PICTURE_HEIGHT):
            for c in range(self.PICTURE_WIDTH):
                pixel = self.image[r][c]
                if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
                    roads.append([c + 1, self.PICTURE_HEIGHT - r])
        return roads

    def search_sensor_by_position(self, point):
        for k, v in self.sensor_position.items():
            if v["x"] == point[0] and v["y"] == point[1]:
                return k
        return None

    def copy_list_by_value(self, old_list):
        new_list = []
        for item in old_list:
            new_list.append(item)
        return new_list

    def find_nearby_recursively(self, current_point, from_points):
        results = {}
        north = [current_point[0], current_point[1] + 1]
        south = [current_point[0], current_point[1] - 1]
        east = [current_point[0] + 1, current_point[1]]
        west = [current_point[0] - 1, current_point[1]]
        next_points = [north, south, west, east]
        for next_point in next_points:
            if max(next_point) <= 200:
                '''if meet a sensor, append it to result'''
                sensor = self.search_sensor_by_position(next_point)
                if sensor != None:
                    '''select the nearest one as the route'''
                    if results.get(sensor, None) != None:
                        old_length = len(results[sensor])
                        new_length = len(from_points)
                        if new_length <= old_length:
                            results[sensor] = from_points
                        #print "after:", len(results[sensor])
                    else:
                        results[sensor] = from_points

                '''if next_point haven't been gone through, then go it recursively'''
                if next_point in self.roads and next_point not in from_points:
                    result = self.find_nearby_recursively(next_point, from_points + [current_point])
                    for k,v in result.items():
                        if results.get(k, None) != None:
                            old_length = len(results[k])
                            new_length = len(result[k])
                            if new_length < old_length:
                                results[k] = v
                        else:
                            results[k] = v
        return results

    def find_all_route(self):
        routes_dict = {}
        for k, v in self.sensor_position.items():
            #print k
            point = [v["x"], v["y"]]
            routes_dict[k] = self.find_nearby_recursively(point, [])
        return routes_dict

    def get_route_points(self, from_sensor, to_sensor):
        if from_sensor in self.route_dict and to_sensor in self.route_dict[from_sensor]:
            route = self.route_dict[from_sensor][to_sensor]
        else:
            raise Exception("Sensors not connected")
        return route

    '''public function, has input check'''
    def get_distance_simple(self, from_sensor, to_sensor):
        if from_sensor in self.route_dict:
            if to_sensor in self.route_dict[from_sensor]:
                return len(self.get_route_points(from_sensor, to_sensor))
            else:
                return self.get_linear_distance(from_sensor, to_sensor)
        else:
            raise Exception("Sensors not exist")

    def get_line_distance(self, from_position, to_position):
        dx = float(from_position[0] - to_position[0])
        dy = float(from_position[1] - to_position[1])
        return math.sqrt(dx**2 + dy**2)

    '''public function, has input check'''
    def get_break_points(self, from_sensor, to_sensor, break_interval = 5):
        if from_sensor in self.route_dict:
            if to_sensor in self.route_dict[from_sensor]:
                route_points = self.get_route_points(from_sensor, to_sensor)
                number_of_break_points = int(len(route_points) / break_interval)
                break_points = []
                for i in range(number_of_break_points):
                    break_points.append(route_points[i * break_interval])
                break_points.append(route_points[-1])
                return break_points
            else:
                raise Exception("Sensors not connected!")
        else:
            raise Exception("Sensors not exist!")

    '''public function, has input check'''
    def get_distance_smart(self, from_sensor, to_sensor, break_interval = 5):
        if from_sensor in self.route_dict:
            if to_sensor in self.route_dict[from_sensor]:
                break_points = self.get_break_points(from_sensor, to_sensor, break_interval)
                distance = 0
                for i in range(len(break_points) - 1):
                    distance += self.get_line_distance(break_points[i], break_points[i+1])
                return distance
            else:
                return self.get_line_distance(from_sensor, to_sensor)
        else:
            raise Exception("Sensors not exist")

    def get_linear_distance(self, from_sensor, to_sensor):
        from_position = self.sensor_position[from_sensor]
        to_position = self.sensor_position[to_sensor]
        dx = from_position["x"] - to_position["x"]
        dy = from_position["y"] - to_position["y"]
        return (float(dx**2 + dy**2)) ** (1/2)

    def save_routes_in_json(self, file_name = "route_distance_dict.json"):
        distance_dict = {}
        for from_sensor, from_position in self.sensor_position.items():
            distance_dict[from_sensor] = {}
            for to_sensor in self.route_dict[from_sensor]:
                distance_dict[from_sensor][to_sensor] = {
                    "distance": self.get_distance_smart(from_sensor, to_sensor),
                    "full_points": self.route_dict[from_sensor][to_sensor],
                    "break_points": self.get_break_points(from_sensor, to_sensor)
                }
        #pprint(distance_dict)

        with open(file_name, 'wb') as f:
            f.write(json.dumps(distance_dict, ensure_ascii=False))

    def save_points_in_json(self, file_name = "point_list.json"):
        points_list = []
        print len(self.roads)
        for point in self.roads:
            points_list.append(point)
        with open(file_name, 'wb') as f:
            f.write(json.dumps(points_list, ensure_ascii=False))


def main():
    '''initialize the class'''
    map_analysis = MapAnalysis()
    #print map_analysis.get_distance_simple("general-gate5", "general-gate5")

    '''should work fine'''
    #print map_analysis.get_route_points("camping1", "general-gate0")
    print "camping1 -> general-gate0:", map_analysis.get_distance_simple("camping1", "general-gate0"),
    print map_analysis.get_distance_smart("camping1", "general-gate0")
    print "ranger-stop3 -> gate3:", map_analysis.get_distance_simple("ranger-stop3", "gate3"),
    print map_analysis.get_distance_smart("ranger-stop3", "gate3")
    #map_analysis.save_routes_in_json()
    map_analysis.save_points_in_json()

    '''should raise exception'''
    #print map_analysis.get_distance_simple("camping1", "entrance0")

    '''test the copy_list_by_value function:
    list_1 = [[1,2],[3,4]]
    list_2 = map_analysis.copy_list_by_value(list_1)
    list_2.append([5,6])
    print list_1
    print list_2
    '''

if __name__ == "__main__":
    main()
