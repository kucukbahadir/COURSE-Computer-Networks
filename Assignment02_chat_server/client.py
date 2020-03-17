"""
M.Bahadir Kucuk 2668015
Tomer Azuz 2658121

Computer Networks Vrije Universiteit
Chat Client Assignment 1

"""

import socket
import threading
import sys


while True:
    # Establishing a connection to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # The parameters specify the network-layer and transport-layer protocol.
    host_port = ("0.0.0.0", 1232)

    sock.connect(host_port)

    # Prompt the user for a username
    username = input("Login with a username:\n")

    # First handshake message
    message = ("HELLO-FROM " + username + "\n").encode("utf-8")

    # sendall calls send repeatedly until all bytes are sent.
    sock.sendall(message)

    # Receive at most 4096 bytes.
    data = sock.recv(4096).decode("utf-8")

    # Check whether the username and the server are available
    if (username):
        if (data == "IN-USE\n"):
            print("Username is already taken.\n")
            sock.close()
            continue
        elif (data == "BUSY\n"):
            print("Maximum number of clients has been reached.")
            sock.close()
            sys.exit()
        else:
            break


# Listen constantly to the server
def listen_server():
    buffer = ""

    while True:
        data = sock.recv(4096).decode("utf-8")
        buffer += data
        messages = buffer.split("\n")
        buffer = messages[-1]

        for single_message in messages[:-1]:

            data_status = single_message.split()[0]

            if (data_status == "SEND-OK"):
                print("‘SEND’ message is processed successfully.")

            elif (data_status == "UNKNOWN"):
                print("The destination user is not currently logged in.")

            elif (data_status == "BAD-RQST-HDR"):
                print("The last message received from the client contains an error in the header.")

            elif (data_status == "BAD-RQST-BODY"):
                print("The last message received from the client contains an error in the body.")
            else:

                message_other_part = single_message[len(data_status) + 1: len(single_message) - 1]

                print(message_other_part)


thread = threading.Thread(target=listen_server, daemon=True)

thread.start()


while True:
    user_input = input()

    if (user_input):
        # to exit the program
        if (user_input == "!quit"):
            sock.close()
            break
        # to see the current users on the server
        elif (user_input == "!who"):

            command = "WHO\n".encode("utf-8")
        # to send a message to a specific user
        elif (user_input[0] == "@"):
            user = user_input.split()[0]

            username = user[1:]
            message = user_input[len(user):]


            command = ("SEND " + username + " " + message + "\n").encode("utf-8")

        else:
            print("Invalid command!")
            continue

        sending = threading.Thread(target=sock.sendall, args=(command,), daemon=True)
        sending.start()

