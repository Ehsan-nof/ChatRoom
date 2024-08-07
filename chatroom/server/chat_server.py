import socket
from threading import Thread, Lock

class chatServer:
    def __init__(self,port=1658,host="127.0.0.1") -> None:
        self.clients={}
        self.threads=[]
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection_lock = Lock()
        self.server.bind((host,port))
            
    def listen(self):
        self.server.listen()
    
    def handle_connection(self,connection:socket, addrress):
        while True:
            raw_data = connection.recv(1024)
            data = raw_data.decode()
            if data == 'q':
                connection.close()
                with self.connection_lock:
                    del self.clients[addrress]
                break
            print("{0}: {1}".format(addrress, data))
            self.broadcast(addrress, data)
            
    def accept(self):
        while True:
            connection, address = self.server.accept()
            with self.connection_lock:
                self.clients[address] = connection
            print("{} is now connected".format(address))
            handle_connection = Thread(target=self.handle_connection,args=(connection, address))
            handle_connection.start()
            self.threads.append(handle_connection)
            with self.connection_lock:
                if not self.clients:
                    for thread in self.threads:
                        thread.join()
    def broadcast(self, self_address, data):
        with self.connection_lock:
            for addr, connection in self.clients.items():
                if addr != self_address:
                    connection.sendall(("{0}: {1}".format(self_address, data)).encode())