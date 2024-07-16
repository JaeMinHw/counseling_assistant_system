from pyfirmata import Arduino, util
import serial.tools.list_ports
import time
from pyfirmata import Arduino, util
from PinManager import PinManager

class ArduinoManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ArduinoManager, cls).__new__(cls)
            cls._instance.board = None
            cls._instance.init_board()
        return cls._instance

    def init_board(self):
        port = self.find_arduino_port()
        if port:
            self.board = Arduino(port)
            it = util.Iterator(self.board)
            it.start()
            self.pin_manager = PinManager(self.board)

    def find_arduino_port(self):
        ports = list(serial.tools.list_ports.comports())
        for port, desc, hwid in sorted(ports):
            if "Arduino" in desc or "VID:PID=2341:0043" in hwid:
                return port
        return None