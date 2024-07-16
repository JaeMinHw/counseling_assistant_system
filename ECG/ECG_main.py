import matplotlib.pyplot as plt
from ArduinoManager import ArduinoManager

data_length = 200
ecg_data = [0] * data_length

def read_ecg():
    board = ArduinoManager()
    # 리드 오프 핀 감지
    lead_off_plus = board.read_sensor(10) == 1
    lead_off_minus = board.read_sensor(11) == 1
    
    # 리드 오프 상태에 따라 LED 색상 변경
    if lead_off_plus or lead_off_minus:
        board.set_led_color(False)  # 빨간색 LED
        return None
    else:
        board.set_led_color(True)  # 파란색 LED
        return board.read_sensor(0) * 3.3  # ECG 센서 데이터 읽기

def update_ecg_graph(data):
    plt.plot(data, label='ECG')
    plt.legend(loc='upper right')
    plt.show()
