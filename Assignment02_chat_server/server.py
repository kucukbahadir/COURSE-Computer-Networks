"""
Tomer Azuz 2658121
Bahadir Kucuk 2668015

Computer Networks Vrije Universiteit AMSTERDAM
Chat Server BONUS Assignment
"""

import socket
import threading
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "0.0.0.0"
port = 1232
address = (IP, port)

server.bind(address)
server.listen(64)  # Max number of clients supported by the server
print("Server started waiting for clients by listening on IP:", IP, " Port:", port)

clients = {}

if "echobot" not in clients:
    clients["echobot"] = None

def receive_message(client_socket,addr):

    if len(clients) <= 64:    # to check whether there are 64 user in the server or not

        while True:

            buffer = ""
            read_check = ""
            ################ BUFFER ###############
            while True:
                read, write, error = select.select([client_socket], [client_socket], [client_socket], 0)
                if read:
                    temp_character = client_socket.recv(1).decode("utf-8")
                    buffer += temp_character
                    read, write, error = select.select([client_socket], [client_socket], [client_socket], 0)
                    if not read:
                        read_check = True
                    if not(buffer):
                        delete_client(client_socket)
                        return

                if (read_check == True):
                    message = buffer.split("\n")
                    buffer = message[-1]
                    break

                ############## END OF BUFFER ##########

            message = "".join(message).split(" ")

            headers = ["HELLO-FROM", "WHO", "SEND", "QUIT"]

            if message[0] == headers[0]:
                handshake(client_socket, message)

            elif message[0] in headers[1:]:

                handle_message(client_socket, message)

            else:
                send_client_message(client_socket, "BAD-RQST-HEAD")

            if not message:
                client_socket.close()
                break
    else:
        send_client_message(client_socket, "BUSY")


def handshake(client_socket, message):

    if len(message) > 1 and message[1].isalnum():
        client_username = message[1]
        # second handshake
        if client_username in clients:
            send_client_message(client_socket, "IN-USE")
        else:
            clients[client_username] = client_socket
            second_handshake_message = "HELLO " + client_username
            send_client_message(client_socket, second_handshake_message)
    else:
        send_client_message(client_socket, "BAD-RQST-BODY")


def handle_message(client_socket, message):

    client_username = get_username(client_socket)

    if message[0] == "WHO":
        answer = "WHO-OK "
        for user in clients.keys():
            answer += user + ","
        send_client_message(client_socket, answer[:-1])

    if message[0] == "SEND":
        if len(message) > 1 and message[1] not in clients.keys():
            send_client_message(client_socket, "UNKNOWN")

        if len(message) > 2 and message[1] in clients:
            client_username = get_username(client_socket)

            if message[1] == "echobot":
                send_client_message(client_socket, " ".join(message[2:]))
            else:
                delivery_message = "DELIVERY " + client_username + " " + " ".join(message[2:])

                send_client_message(clients[message[1]], delivery_message)
                send_client_message(client_socket, "SEND-OK")
        else:
            send_client_message(client_socket, "BAD-RQST-BODY")

    if message[0] == "QUIT":
        client_socket.close()
        delete_client(client_socket)

    print("Processing done.\n" "Reply sent")


def get_username(client_socket):
    if client_socket in clients.values():
        for key, value in clients.items():
            if client_socket == value:
                return key

def delete_client(client_socket):

    client_username = get_username(client_socket)

    if client_username in clients:
        del clients[client_username]

def send_client_message(client_socket, message):

    client_socket.send(bytes(message + "\n", "utf-8"))


while True:
    socket, addr = server.accept()
    print("A new client connection --> {} : {}".format(socket, addr))

    client_Thread = threading.Thread(target=receive_message, args=(socket, addr), daemon=True)
    client_Thread.start()











