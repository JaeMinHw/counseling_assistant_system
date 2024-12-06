# import main

# # main.main()

# import socketio

# sio = socketio.Client()

# @sio.event
# def connect():
#     print("I'm connected!")

# @sio.event
# def disconnect():
#     print("I'm disconnected!")

# @sio.event
# def sensor_start():
#     print("sensor_start")  # 서버로부터 받은 메시지 출력
#     # 그러면 이제 센서 측정하는 코드 실행

# sio.connect('http://192.168.0.72:5000',transports=['websocket'])

# try:
#     # 클라이언트가 계속 실행되도록 합니다.
#     sio.wait()
# except KeyboardInterrupt:
#     sio.disconnect()


import socketio
import random
import time
from threading import Event, Thread

sio = socketio.Client()
stop_event = Event()


@sio.event
def connect():
    print("I'm connected!")
    # 환자 로그인 이벤트 서버로 전송
    sio.emit('patient_login', {'patient_id': 'woals99', 'counselor_id': 'counselor_1'})

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.event
def connection_accepted(data):
    print(f"Connection accepted: {data}")
    # sio.emit('sensor_start')  # 서버로부터 연결 수락 메시지를 받으면 센서 시작


def start_sending_data(room):
    while True:
        # 임의의 데이터 생성 (센서 데이터)
        data1 = random.uniform(0, 100)
        data2 = random.uniform(0, 100)
        data3 = random.uniform(0, 100)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        # 서버로 데이터 전송
        sio.emit('sensor_data', {'room': room,'data1': data1, 'data2': data2, 'data3': data3, 'time': current_time})
        print(f"Sent data: {room}, {data1}, {data2}, {data3} at {current_time}")
        
        time.sleep(0.1)  # 0.1초마다 데이터 전송


@sio.event
def sensor_start(room):
    print(f"sensor_start: {room}")  # 서버로부터 받은 메시지 출력
    # 여기서 센서 측정하는 코드를 실행
    start_sending_data(room)
    # 데이터 임의로 생성 후 stop 신호가 오기 전까지 계속 서버로 전송


@sio.event
def stop():
    pass

sio.connect('http://127.0.0.1:5000', transports=['websocket'])

try:
    # 클라이언트가 계속 실행되도록 합니다.
    sio.wait()
except KeyboardInterrupt:
    sio.disconnect()
