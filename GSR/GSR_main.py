# GSR_main.py
import matplotlib.pyplot as plt
from ArduinoManager import ArduinoManager

data_length = 200
gsr_data = [0] * data_length

def read_gsr():
    board = ArduinoManager()
    print(board.read_sensor(1))
    return board.read_sensor(1)

def update_gsr_graph(data):
    plt.plot(data, label='GSR')
    plt.legend(loc='upper right')
    plt.show()
