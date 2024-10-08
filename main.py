import matplotlib.pyplot as plt
import time
import sys

# sys.path.append('C:/Users/user/Desktop/counseling_assistant_system/ECG')
sys.path.append('C:/Users/user/Desktop/counseling_assistant_system/GSR')


from ECG.ECG_main import read_ecg, update_ecg_graph
from GSR.GSR_main import read_gsr, update_gsr_graph

data_length = 200
ecg_data = [0] * data_length
gsr_data = [0] * data_length

def update_graphs():
    plt.subplot(2, 1, 1)  # 2행 1열의 첫 번째 그래프
    plt.cla()  # 현재 그래프 지우기
    if ecg_data[0] is None:  # 첫 번째 데이터를 기준으로 리드 오프 상태 확인
        plt.plot([0]*data_length, label='ECG', color='red')
        plt.title('ECG Data - Detected lead-off!')
    else:
        plt.plot(ecg_data, label='ECG')
        plt.title('ECG Data')
    plt.legend(loc='upper right')

    plt.subplot(2, 1, 2)  # 2행 1열의 두 번째 그래프
    plt.cla()  # 현재 그래프 지우기
    plt.plot(gsr_data, label='GSR')
    plt.title('GSR Data')
    plt.legend(loc='upper right')

    plt.pause(0.05)  # 그래프 업데이트를 위한 일시 중지

def main():
    plt.ion()  # 인터랙티브 모드 활성화
    while True:
        ecg_voltage = read_ecg()
        gsr_voltage = read_gsr()

        if ecg_voltage is None:
            ecg_data[0] = None  # 리드 오프 상태를 첫 번째 데이터에 표시
        else:
            ecg_data.append(ecg_voltage)
            ecg_data.pop(0)

        if gsr_voltage is not None:
            gsr_data.append(gsr_voltage)
            gsr_data.pop(0)

        update_graphs()

if __name__ == "__main__":
    main()