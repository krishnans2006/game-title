import websockets


class Connection:
    def __init__(self):
        self.host = self.port = self.connection = None

    def connect(self, host, port):
        self.host = host
        self.port = port
        self.connection = websockets.connect(f"ws://{host}:{port}")
