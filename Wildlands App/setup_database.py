from Webapplicatie import db, Verblijf
from Webapplicatie.models import *
import random
import names

db.create_all()

serenga = Verblijf('Serenga')
jungola = Verblijf('Jungola')
nortica = Verblijf('Nortica')
animazia = Verblijf('Animazia')
test = Verblijf('Test')

db.session.add_all([serenga, jungola, nortica, animazia, test])
ijsberen = Diersoort('Ijsbeer')
db.session.add_all([ijsberen])

# Henk = Dier('Ijsbeer', 'Henk', True,'0009', 'Nortica')
# db.session.add_all([Henk])

db.session.commit()

witte_neushoorn = Diersoort('Witte neushoorn')
nijlpaard = Diersoort('Nijlpaard')
ringstaartmaki = Diersoort('Ringstaartmaki')
zuidelijke_pelsrob = Diersoort('Zuidelijke pelsrob')
bonte_vari = Diersoort('Bonte vari')
groene_zeeschildpad = Diersoort('Groene zeeschildpad')
sporenschildpad = Diersoort('Sporenschildpad')

db.session.add_all([witte_neushoorn, nijlpaard, ringstaartmaki, zuidelijke_pelsrob, bonte_vari, groene_zeeschildpad, sporenschildpad])

# Dieren = []
# verblijven = []
# for i in Verblijf.query.all():
#     verblijven += i.name

# for i in Diersoort.query.all():
#     for j in range(random.randint(3,5)):
#         Dieren += [Dier(i.name, names.get_first_name(), True, random.choice(verblijven))] 

L = []
for i in range(10):
    q = Device(str(i))
    L.append(q) 
    
db.session.add_all(L)

Witte_neushoorn = Dier('Witte neushoorn', 'Witte neushond', True, 0, 'Serenga')
Nijlpaard = Dier('Nijlpaard', 'Nijlpaard', True, 1, 'Animazia')
Ringstaartmaki = Dier('Ringstaartmaki', 'Ringstaartmaki',False, 2, 'Serenga')
Zuidelijke_pelsrob = Dier('Zuidelijke pelsrob', 'Zuidelijke pelsrob', True, 3, 'Jungola')
Bonte_vari = Dier('Bonte vari', 'Bonte vari', True,4, 'Jungola')
Groene_zeeschildpad = Dier('Groene zeeschildpad', 'Groene zeeschildpad', False,5, 'Animazia')
Sporenschildpad = Dier('Sporenschildpad', 'Sporenschildpad', True, 6, 'Animazia')



pieter = Dier('Nijlpaard', 'Pieter', True,7, 'Nortica')
db.session.add_all([pieter, Witte_neushoorn, Nijlpaard, Ringstaartmaki, Zuidelijke_pelsrob, Bonte_vari, Groene_zeeschildpad, Sporenschildpad])

db.session.commit()

testdier = Dier('Nijlpaard', 'Test', True, 1, 'Test')
lois = Dier('Nijlpaard', 'Lois', True, 1, 'Test')
sensor1 = Sensor(5, 7.5, 7.5)
sensor2 = Sensor(5, 5, -5)
sensor3 = Sensor(5, 0, -2.5)

db.session.add_all([lois, testdier, sensor1, sensor2, sensor3])
db.session.commit()

output1 = Data(1, 9, 7.0)
output2 = Data(2, 9, 6.0)
output3 = Data(3, 9, 8.0)

output4 = Data(1, 10, 7.9)
output5 = Data(2, 10, 5.0)
output6 = Data(3, 10, 5.6)


db.session.add_all([output1, output2, output3, output4, output5, output6])
db.session.commit()


# db.session.add_all([ijsberen])
# db.session.commit