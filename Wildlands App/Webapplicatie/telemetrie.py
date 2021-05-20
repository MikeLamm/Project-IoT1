import numpy as np
import matplotlib.pyplot as plt
import math
from Webapplicatie import db
from Webapplicatie.models import *
import os

my_path = os.path.abspath(__file__)


class Telemetrie():
    def __init__(self, stay, beacon1, beacon2, beacon3):
        self.beacon1 = beacon1
        self.beacon2 = beacon2
        self.beacon3 = beacon3
        self.points = {}
        self.location = []

    def get_intersections(self, x0, y0, r0, x1, y1, r1):
        # circle 1: (x0, y0), radius r0
        # circle 2: (x1, y1), radius r1

        d=math.sqrt((x1-x0)**2 + (y1-y0)**2)

        # non intersecting
        if d > r0 + r1 :
            print(1)
            return {}
        # One circle within other
        if d < abs(r0-r1):
            print(2)
            return {}
        # coincident circles
        if d == 0 and r0 == r1:
            print(3)
            return {}
        else:
            a=(r0**2-r1**2+d**2)/(2*d)
            h=math.sqrt(r0**2-a**2)
            x2=x0+a*(x1-x0)/d   
            y2=y0+a*(y1-y0)/d   
            x3=x2+h*(y1-y0)/d     
            y3=y2-h*(x1-x0)/d 
            x4=x2-h*(y1-y0)/d
            y4=y2+h*(x1-x0)/d
            a = round(x3,1)
            b = round(y3,1)
            c = round(x4,1)
            d = round(y4,1)
            self.points['first'] = [a,b]
            self.points['second'] = [c,d]
            return self.points
    
    def start(self):
        x0, y0, r0 = self.beacon1
        x1, y1, r1 = self.beacon2
        x2, y2, r2 = self.beacon3

        # print(self.get_intersections(x0, y0, r0, x1, y1, r1))
        # print(self.get_intersections(x0, y0, r0, x2, y2, r2))
        # print(self.get_intersections(x1, y1, r1, x2, y2, r2))

        a = self.get_intersections(x0, y0, r0, x1, y1, r1)
        b = self.get_intersections(x0, y0, r0, x2, y2, r2)
        c = self.get_intersections(x1, y1, r1, x2, y2, r2)
        print(a.values(), b.values(), c.values())

        if a == {}:
            self.location = False
            print(self.location)
            return self.location
        elif a['first'] in b.values() and c.values():
            self.location = a['first']
            print(self.location)
            return self.location
        elif a['second'] in b.values() and c.values():
            self.location = a['second']
            print(self.location)
            return self.location
            
        # circle1 = plt.Circle((x0, y0), r0, color='b', fill=False)
        # circle2 = plt.Circle((x1, y1), r1, color='b', fill=False)
        # circle3 = plt.Circle((x2, y2), r2, color='b', fill=False)

        # self.axes.add_artist(circle1)
        # self.axes.add_artist(circle2)
        # self.axes.add_artist(circle3)

        # plt.show()
        
class Create_Map():
    def __init__(self, stay):
        self.list_of_animals = Dier.query.filter_by(verblijf=stay.id).all()
        print(f'Lijst van dieren {self.list_of_animals}')
        self.figure, self.axes = plt.subplots()
        self.map = [(-10,10), (-10,10)]
        self.stay = stay
        self.axes.set(xlim=self.map[0], ylim=self.map[1])
        self.axes.set_axis_off()
        self.figure.edgecolor = 'black'
        # plt.title(self.stay.name)
        

    def create_map(self):
        for i in self.list_of_animals:
            if i.detected:
                print(i.id)
                print(Data.query.filter_by(dier=i.id).all())
                x = [j.x for j in Sensor.query.filter_by(verblijf=self.stay.id).all()]
                print
                y = [j.y for j in Sensor.query.filter_by(verblijf=self.stay.id).all()]
                output = [j.output for j in Data.query.filter_by(dier=i.id).all()]
                    
                beacon1 = [x[0], y[0], float(output[0])]
                plt.scatter(beacon1[0], beacon1[1], color='red')
                beacon2 = [x[1], y[1], float(output[1])]
                plt.scatter(beacon2[0], beacon2[1], color='red')
                beacon3 = [x[2], y[2], float(output[2])]
                plt.scatter(beacon3[0], beacon3[1], color='red')
                print(beacon1,beacon2,beacon3)
                location = Telemetrie(((-10,10), (-10,10)), beacon1, beacon2, beacon3)
                location = location.start()
                print(f'Locatie {location}')
                x, y = location
                plt.scatter(x, y)
                plt.annotate(i.name, (x, y))
        self.figure.savefig(f'Webapplicatie/static/maps/{self.stay.name}', transparent=True)

        
        



if __name__ == '__main__':
    # print(get_intersections(1, 1, 5, -5, 5, 5))
    # plot()
    # x = Telemetrie(((-10,10), (-10,10)), [7.5,7.5,7.9], [5,-5,5.0], [0,-2.5,5.6])
    # x.start()
    stay = Verblijf.query.get(5)
    map = Create_Map(stay)
    map.create_map()
