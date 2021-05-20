from Webapplicatie import *
from Webapplicatie.views import *
from Webapplicatie.models import *
from Webapplicatie.telemetrie import *
from Webapplicatie.message import *
import time
import threading

def refresh_map():
    stays = Verblijf.query.all()
    for i in stays:
        map = Create_Map(i)
        map.create_map()
            
        
def check_presence():
    for i in Data.query.all():
        if i.output is None:
            animal = Dier.query.filter_by(id=i.dier).first()
            animal.detected = False
            db.session.add(animal)
            db.session.commit()
        else:
            animal = Dier.query.filter_by(id=i.dier).first()
            animal.detected = True
            db.session.add(animal)
            db.session.commit()

L = []
def alert():
    for i in Dier.query.all():
        stay = Verblijf.query.filter_by(id=i.verblijf).first()
        if i.name in L:
            if i.detected:
                L.remove(i.name)
        else:
            if i.detected == False:
                L.append(i.name)
                msg = SendPushNotification(i.name, stay.name)
                msg.Send()


def run():
    while True:
        check_presence()
        refresh_map()
        alert()
        time.sleep(15)
        
if __name__ == '__main__':
    thread0 = threading.Thread(target=run)
    thread1 = threading.Thread(target=app.run)
    thread0.start()
    thread1.start()
    