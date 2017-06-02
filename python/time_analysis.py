import csv
from datetime import datetime

count_by_time = [[0] * 24 for row in range(7)]
count1_by_time = [[0] * 24 for row in range(7)]
count2_by_time = [[0] * 24 for row in range(7)]
count3_by_time = [[0] * 24 for row in range(7)]
count4_by_time = [[0] * 24 for row in range(7)]
count5_by_time = [[0] * 24 for row in range(7)]
count6_by_time = [[0] * 24 for row in range(7)]
count2P_by_time = [[0] * 24 for row in range(7)]

with open("Lekagul Sensor Data.csv","rb") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=",", quotechar="|")
    i = 0
    for row in spamreader:
        i += 1
        #if i > 100:
        #    break
        if i == 1:
            continue
        else:
            dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            count_by_time[dt.weekday()][dt.hour] += 1
            if row[2] == '1':
                count1_by_time[dt.weekday()][dt.hour] += 1
            if row[2] == '2':
                count2_by_time[dt.weekday()][dt.hour] += 1
            if row[2] == '3':
                count3_by_time[dt.weekday()][dt.hour] += 1
            if row[2] == '4':
                count4_by_time[dt.weekday()][dt.hour] += 1
            if row[2] == '5':
                count5_by_time[dt.weekday()][dt.hour] += 1
            if row[2] == '6':
                count6_by_time[dt.weekday()][dt.hour] += 1
            if row[2] == '2P':
                count2P_by_time[dt.weekday()][dt.hour] += 1
    for d in range(7):
        for t in range(24):
            print "["+str(d)+", "+str(t)+", "+str(count2P_by_time[d][t])+"],"
