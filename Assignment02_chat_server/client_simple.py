import socket
import threading

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_STREAM)  # The parameters specify the network-layer and transport-layer protocol.

host_port = ("0.0.0.0", 1232)

sock.connect(host_port)

def send_message():
    while True:
        sock.send(bytes(input("Enter message: "), "utf-8"))


iThread = threading.Thread(target=send_message)
iThread.daemon = True
iThread.start()

while True:
    data = sock.recv(1024)
    if not data:
        break
    print(str(data, "utf-8"))

