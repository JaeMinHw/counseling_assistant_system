# PinManager.py
class PinManager:
    def __init__(self, board):
        self.board = board
        self.setup_pins()

    def setup_pins(self):
        # LED 핀 설정
        self.led_pin = self.board.get_pin('d:13:o')
        # ECG 핀 설정
        self.ecg_input = self.board.get_pin('a:0:i')
        self.lead_off_plus = self.board.get_pin('d:10:i')
        self.lead_off_minus = self.board.get_pin('d:11:i')
        # GSR 핀 설정
        self.gsr_input = self.board.get_pin('a:1:i')

    def set_led_state(self, is_connected):
        # LED 상태 설정
        self.led_pin.write(1 if is_connected else 0)

    def read_ecg(self):
        # ECG 데이터 읽기
        if self.lead_off_plus.read() == 1 or self.lead_off_minus.read() == 1:
            self.set_led_state(False)
            return None
        else:
            self.set_led_state(True)
            return self.ecg_input.read()

    def read_gsr(self):
        # GSR 데이터 읽기
        return self.gsr_input.read()

