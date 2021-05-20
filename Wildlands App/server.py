import socket
from Webapplicatie import db
from Webapplicatie.models import *




class Server:
    """ The host or 'server' for the esp32.

        Takes 3 arguments:\n
        list_of_animals, a list of the animals that need to be tracked.\n
        host_ip, the (string) ip of the host/server (where this code is ran)\n
        host_port, the port to create the socket on."""

    def __init__(self, list_of_animals, host_ip, host_port):
        self.socket = socket.socket()
        self.host = host_ip
        self.port = host_port
        self.socket.bind((self.host, self.port))
        self.conn = ''
        self.list_of_animals = list_of_animals
        self.list_of_devices = []
        self.last_message = ''

    def establish_connection(self):
        """ Listens for a connection.
        """
        print('Listening...')
        self.socket.listen()
        self.conn, addr = self.socket.accept()
        print('Received connection', addr)

    def receive_data(self, conn):
        """Receive and process initial data (requires a connection before running.)"""
        data = conn.recv(2048)
        message = data.decode('utf-8')
        currDev = ''
        if message != self.last_message and message != '':
            if len(message) >= 24:
                for letter in message:
                    currDev += letter
                    if len(currDev) == 12:
                        self.list_of_devices += [currDev]
                        currDev = ''
            else:
                self.list_of_devices = [message]

        print(self.list_of_devices)

    def run_server(self):
        """ run_server runs the server... (makes a connection and loops receive_data())"""
        self.establish_connection()
        while True:
            self.receive_data(self.conn)

class UpdateDatabase:
    def __init__(self, list_of_devices):
        self.db = db
        self.list_of_devices = list_of_devices
        self.list_of_animals = []

    def check_for_presence(self):
        q = Dier.query.all()
        missing_animals = []
        for i in q:
            self.list_of_animals.append(i)
        for j in self.list_of_animals:
            if j.device not in self.list_of_devices:
                print(j.device)
                print(self.list_of_devices)
                missing_animals.append(j)
        for k in missing_animals:
            dier = Dier.query.filter_by(device=k.id).first()
            dier.detected = False
            self.db.session.add_all([dier])
        self.db.session.commit()
        

    def start(self):
        self.check_for_presence()








# list_of_animals = []
# server1 = Server(list_of_animals, '192.168.137.1', 8003)

L = [0,1,2,3,4,5,6,7]
update = UpdateDatabase(L)
if __name__ == "__main__":
    # server1.run_server()
    update.start()
