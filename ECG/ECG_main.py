# ECG_main.py
import matplotlib.pyplot as plt
from ArduinoManager import ArduinoManager

data_length = 200
ecg_data = [0] * data_length

def read_ecg():
    board = ArduinoManager()
    return board.read_sensor(0)

def update_ecg_graph(data):
    plt.plot(data, label='ECG')
    plt.legend(loc='upper right')
    plt.show()
