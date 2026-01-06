import socket
import msgpack

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.100.112"
        self.port = 5050
        self.addr = (self.server, self.port)
        # store last-known player dict from server (initial state)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            raw = self.client.recv(2048)
            if not raw:
                return None
            data = msgpack.unpackb(raw, raw=False)
            # return plain dict to caller; client will convert to sprites
            return data
        except socket.error as e:
            print(e)
        

    def send(self, data):
        try:
            # data should be a plain dict. Pack and send, then unpack reply dict.
            payload = msgpack.packb(data, use_bin_type=True)
            self.client.send(payload)
            raw = self.client.recv(2048)
            if not raw:
                return None
            resp = msgpack.unpackb(raw, raw=False)
            return resp
        except socket.error as e:
            print(e)
    # Network class intentionally does not construct sprite objects.
    # It sends and receives plain dicts representing player state.
            