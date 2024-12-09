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
from threading import Thread, Event

sio = socketio.Client()
stop_events = {}  # 각 room별로 stop 이벤트 관리


@sio.event
def connect():
    print("I'm connected!")
    sio.emit('patient_login', {'patient_id': 'woals99', 'counselor_id': 'counselor_1'})

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.event
def connection_accepted(data):
    print(f"Connection accepted: {data}")



# 센서 데이터 읽기 함수 (실제 센서 함수로 교체)
def read_all_sensors():
    """
    모든 센서 데이터를 동시에 읽음.
    """
    sensor1_data = random.uniform(0, 100)  # 센서1 데이터 읽기
    sensor2_data = random.uniform(0, 100)  # 센서2 데이터 읽기
    sensor3_data = random.uniform(0, 100)  # 센서3 데이터 읽기
    return sensor1_data, sensor2_data, sensor3_data

def start_sending_data(room):
    stop_event = stop_events[room]
    while not stop_event.is_set():  # stop_event가 설정되기 전까지 실행

        data1, data2, data3 = read_all_sensors()
        
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        sio.emit('sensor_data', {
            'room': room,
            'data1': data1,
            'data2': data2,
            'data3': data3,
            'time': current_time
        })
        print(f"Sent data: Room {room}, {data1}, {data2}, {data3} at {current_time}")
        time.sleep(1/60)  # 0.1초마다 데이터 전송

    print(f"Stopped sending data for room {room}")

@sio.event
def sensor_start(data):
    room =data  # 서버로부터 room 정보 추출
    print(f"Starting sensor for room {room}")
    if room not in stop_events:
        stop_events[room] = Event()
        thread = Thread(target=start_sending_data, args=(room,))
        thread.daemon = True
        thread.start()
    else:
        print(f"Sensor already running for room {room}")

@sio.event
def stop(data):
    room = data  # 서버로부터 room 정보 추출
    if not room:
        print("No room specified in stop event")
        return

    print(f"Stopping sensor for room {room}")
    if room in stop_events:
        stop_events[room].set()  # stop_event를 설정하여 루프 종료
        del stop_events[room]  # stop_event 제거
        print(f"Sensor stopped for room {room}")
    else:
        print(f"No active sensor for room {room}")

sio.connect('http://127.0.0.1:5000', transports=['websocket'])

try:
    sio.wait()
except KeyboardInterrupt:
    for event in stop_events.values():
        event.set()  # 모든 stop_event 설정
    sio.disconnect()
