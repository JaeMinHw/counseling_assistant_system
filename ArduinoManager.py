from pyfirmata import Arduino, util
import serial.tools.list_ports
import time

class ArduinoManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ArduinoManager, cls).__new__(cls)
            cls._instance.board = None
            cls._instance.pins = {}
            cls._instance.init_board()
        return cls._instance

    def init_board(self):
        port = self.find_arduino_port()
        if port:
            self.board = Arduino(port)
            it = util.Iterator(self.board)
            it.start()

    def find_arduino_port(self):
        ports = list(serial.tools.list_ports.comports())
        for port, desc, hwid in sorted(ports):
            if "Arduino" in desc or "VID:PID=2341:0043" in hwid:
                return port
        return None

    def get_pin(self, pin_number, mode='i'):
        key = (pin_number, mode)
        if key not in self.pins:
            if mode == 'a':  # 아날로그 모드를 위한 설정
                self.pins[key] = self.board.get_pin(f'a:{pin_number}:{mode}')
            else:  # 디지털 모드를 위한 설정
                self.pins[key] = self.board.get_pin(f'd:{pin_number}:{mode}')
        return self.pins[key]


    def read_sensor(self, pin_number, mode='a'):  # 아날로그 모드가 기본값
        pin = self.get_pin(pin_number, mode)
        if pin is not None:
            time.sleep(0.1)  # 핀 초기화와 데이터 안정화를 위한 지연
            value = pin.read()
            if value is None:
                print(f"핀 {pin_number}에서 데이터를 읽지 못했습니다.")
                return None
            return value * 3.3  # 센서 값 조정
        else:
            raise Exception("핀 설정이 잘못되었습니다.")
    
    def read_digital(self, pin_number):
        pin = self.get_pin(pin_number, 'i')
        if pin is not None:
            return pin.read()
        else:
            raise Exception("핀 설정이 잘못되었습니다.")