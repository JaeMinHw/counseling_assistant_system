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

sio = socketio.Client()

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
    sio.emit('sensor_start')  # 서버로부터 연결 수락 메시지를 받으면 센서 시작

@sio.event
def sensor_start():
    print("sensor_start")  # 서버로부터 받은 메시지 출력
    # 여기서 센서 측정하는 코드를 실행



sio.connect('http://192.168.0.72:5000', transports=['websocket'])

try:
    # 클라이언트가 계속 실행되도록 합니다.
    sio.wait()
except KeyboardInterrupt:
    sio.disconnect()
