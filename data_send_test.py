import socketio
import random
import time
from threading import Thread, Event

sio = socketio.Client()
stop_events = {}  # 각 room별로 stop 이벤트 관리
data1_buffer = []  # data1 배치 전송을 위한 버퍼


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


# 센서 데이터 생성 함수
def generate_data1():
    return random.uniform(0, 100)


def generate_data2():
    return random.uniform(0, 100)


def generate_data3():
    return random.uniform(0, 100)


def batch_send_data1(room):
    """
    data1을 배치로 전송.
    """
    global data1_buffer
    batch_interval = 0.1  # 100ms마다 배치 전송

    while not stop_events[room].is_set():
        stop_events[room].wait(batch_interval)  # 대기 중에도 stop_event 확인
        if data1_buffer:
            batch = data1_buffer[:]
            data1_buffer = []

            sio.emit('sensor_data_batch', {
                'room': room,
                'data1_batch': batch,
                'time': time.strftime('%Y-%m-%d %H:%M:%S')
            })
            print(f"Sent batch data1: {batch}")


def send_data2(room):
    """
    data2를 즉시 전송.
    """
    while not stop_events[room].is_set():
        data2 = generate_data2()
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        sio.emit('sensor_data', {
            'room': room,
            'sensor': 'data2',
            'value': data2,
            'time': current_time
        })
        print(f"Sent data2: {data2} at {current_time}")
        if stop_events[room].wait(1 / 60):  # 60Hz 주기 동안 stop_event 확인
            break


def send_data3(room):
    """
    data3를 즉시 전송.
    """
    while not stop_events[room].is_set():
        data3 = generate_data3()
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        sio.emit('sensor_data', {
            'room': room,
            'sensor': 'data3',
            'value': data3,
            'time': current_time
        })
        print(f"Sent data3: {data3} at {current_time}")
        if stop_events[room].wait(1 / 60):  # 60Hz 주기 동안 stop_event 확인
            break


def start_sending_data(room):
    """
    센서 데이터 전송을 시작하는 함수.
    """
    global data1_buffer
    stop_event = stop_events[room]

    # 배치 전송 스레드
    batch_thread = Thread(target=batch_send_data1, args=(room,))
    batch_thread.daemon = True
    batch_thread.start()

    # 즉시 전송 스레드
    data2_thread = Thread(target=send_data2, args=(room,))
    data2_thread.daemon = True
    data2_thread.start()

    data3_thread = Thread(target=send_data3, args=(room,))
    data3_thread.daemon = True
    data3_thread.start()

    # data1을 생성하여 버퍼에 저장
    while not stop_event.is_set():
        data1 = generate_data1()
        data1_buffer.append(data1)
        if stop_event.wait(1 / 500):  # 500Hz 주기 동안 stop_event 확인
            break


@sio.event
def sensor_start(data):
    room = data  # 서버로부터 room 정보 추출
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
        del stop_events[room]
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
