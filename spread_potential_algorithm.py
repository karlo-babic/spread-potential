import csv
import datetime as dt


FILENAME = "data_original.csv"
MIN_WAIT_TIME = dt.timedelta(minutes=30)
MAX_WAIT_TIME = dt.timedelta(minutes=180)

##################################################################################

print("\nloading data by PDEP...")

data_pdep = {}
with open(FILENAME) as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    for i, row in enumerate(reader):
        if i == 0: continue
        if row[0] == "": continue
        if i%1000 == 0: print("  line:", str(i))
        
        # sample: 10.8.2015 13:30
        row[0] = dt.datetime.strptime(row[0], "%d.%m.%Y %H:%M")
        row[2] = dt.datetime.strptime(row[2], "%d.%m.%Y %H:%M")
        row[4] = int(row[4])
        link = {"time_departure": row[0], "port_departure": row[1], "time_arrival": row[2], "port_arrival": row[3], "weight": row[4]}
        if row[1] in data_pdep:
            data_pdep[link["port_departure"]].append(link)
        else:
            data_pdep[link["port_departure"]] = [link]

#print("\nports: " + str( list(data_pdep.keys()) ))

for key in data_pdep.keys():
    data_pdep[key].sort(key=lambda x: x["time_departure"])

##################################################################################

print("\nsumming paths...")

def _path_sum_rec(link, visited_ports=[], previous_sum=0):
    previous_sum += link["weight"]
    partial_sum = previous_sum
    key = link["port_arrival"]
    if key not in data_pdep: return partial_sum
    visited_ports.append(link["port_departure"])
    visited_ports_fromthispot = []
    for next_link in data_pdep[key]:
        if next_link["port_arrival"] in visited_ports:
            continue
        if next_link["time_departure"] - link["time_arrival"] >= MIN_WAIT_TIME and next_link["time_departure"] - link["time_arrival"] <= MAX_WAIT_TIME:
            if next_link["port_arrival"] in visited_ports_fromthispot:
                pass
            visited_ports_fromthispot.append(next_link["port_arrival"])
            partial_sum += _path_sum_rec(next_link, visited_ports.copy(), previous_sum)
    return partial_sum

def path_sum(starting_departure):
    total_sum = _path_sum_rec(starting_departure, visited_ports=[])
    return total_sum

##################################################################################

sums = []
for key in data_pdep.keys():
    dep_sum = 0
    for link in data_pdep[key]:
        dep_sum += path_sum(link)
    sums.append(dep_sum)
    print(key, dep_sum, sep=';')

print("\n\nsum of path sums:", sum(sums))
