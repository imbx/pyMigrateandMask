import csv, os
import numpy

def SaveCSV(filename, data):
    a = numpy.array(data)
    with open(os.path.join("./output/", filename), 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(a)