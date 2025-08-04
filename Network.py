import socket
import pickle

class NetWork():
    def __init__(self, serverIp):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = serverIp
        self.port = 5555
        self.addr = (self.server, self.port)
        self.__data = self.connect()

    def getData(self):
        return self.__data

    def connect(self):
        try:
            self._client.connect(self.addr)
            return pickle.loads(self._client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self._client.send(pickle.dumps(data))
            return pickle.loads(self._client.recv(2048))
        except socket.error as e:
            print(e)


