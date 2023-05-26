import socket
import protocol
from datetime import datetime
import random


SERVER_NAME = "My Server"


def create_server_rsp(cmd):
    if cmd == 'TIME':
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if cmd == 'WHORU':
        return SERVER_NAME
    if cmd == 'RAND':
        return str(random.randint(1, 10))
    if cmd == 'EXIT':
        return 'EXIT'


def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("0.0.0.0", protocol.PORT))
        server_socket.listen()
        print("Server is up and running")
        client_socket, client_address = server_socket.accept()
        print(f"client connected: {client_address}")

        with client_socket:
            while True:
                valid_msg, cmd = protocol.get_msg(client_socket)

                if valid_msg:
                    print(f'server received from user: {cmd}')

                    if protocol.check_cmd(cmd):
                        response = create_server_rsp(cmd)
                    else:
                        response = "Wrong command"
                else:
                    response = "Wrong protocol \n" + cmd
                    client_socket.recv(1024)  # Attempt to empty the socket from possible garbage

                if cmd == 'EXIT':
                    break

                response = protocol.create_msg(response)
                client_socket.send(response.encode())


if __name__ == "__main__":
    main()
