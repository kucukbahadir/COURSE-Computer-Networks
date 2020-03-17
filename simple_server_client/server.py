import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "0.0.0.0"
port = 1234
address = (IP, port)

server.bind(address)

server.listen(64)

clients = []


def handler(c,a):
    global clients
    while True:
        data = c.recv(1024)
        print(data.decode("utf-8"))

        if not data:
            clients.remove(c)
            c.close()
            break

def send_message():
    while True:
        print("client: ", clients[0])
        print(type(clients[0]))
        clients[0].send(bytes(input("Enter message: "), "utf-8"))

while True:
    c, a = server.accept()
    cThread = threading.Thread(target=handler, args=(c, a))
    cThread.daemon = True
    cThread.start()
    clients.append(c)
    print(clients)
    print("connected")

    send_message()

