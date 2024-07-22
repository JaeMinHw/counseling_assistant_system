import matplotlib.pyplot as plt
from ArduinoManager import ArduinoManager

data_length = 200
ecg_data = [0] * data_length

def read_ecg():
    board = ArduinoManager()
    # 리드 오프 상태 검사
    if board.read_digital(10) == 1 or board.read_digital(11) == 1:
        return None  # 리드 오프 상태면 None 반환
    else:
        return board.read_sensor(0)  # 아날로그 값 읽고 반환

def update_ecg_graph(data):
    plt.plot(data, label='ECG')
    plt.legend(loc='upper right')
    plt.show()
