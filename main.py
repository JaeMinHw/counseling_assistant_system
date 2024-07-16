# main.py
import matplotlib.pyplot as plt
import time
import sys

# sys.path.append('C:/Users/user/Desktop/counseling_assistant_system/ECG')
sys.path.append('C:/Users/user/Desktop/counseling_assistant_system/GSR')


from ECG.ECG_main import read_ecg, update_ecg_graph
from GSR.GSR_main import read_gsr, update_gsr_graph


from ArduinoManager import ArduinoManager

data_length = 200
ecg_data = [0] * data_length
gsr_data = [0] * data_length

def update_graphs():
    plt.subplot(2, 1, 1)
    plt.cla()
    plt.plot(ecg_data, label='ECG')
    plt.title('ECG Data')
    plt.legend(loc='upper right')

    plt.subplot(2, 1, 2)
    plt.cla()
    plt.plot(gsr_data, label='GSR')
    plt.title('GSR Data')
    plt.legend(loc='upper right')

    plt.pause(0.05)

def main():
    plt.ion()
    arduino_manager = ArduinoManager()
    while True:
        ecg_voltage = arduino_manager.pin_manager.read_ecg()
        gsr_voltage = arduino_manager.pin_manager.read_gsr()

        if ecg_voltage is not None:
            ecg_data.append(ecg_voltage)
            ecg_data.pop(0)

        if gsr_voltage is not None:
            gsr_data.append(gsr_voltage)
            gsr_data.pop(0)

        update_graphs()

if __name__ == "__main__":
    main()
