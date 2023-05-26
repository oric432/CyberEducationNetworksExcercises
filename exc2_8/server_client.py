import random
import socket


class ServerClient:

    SERVER_ROLE = 'SERVER'
    CLIENT_ROLE = 'CLIENT'

    def __init__(self, role, port, ip):
        self.ip = ip
        self.port = port
        self.role = role

    def __server_role(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as side_a_socket:
            side_a_socket.bind((self.ip, self.port))
            side_a_socket.listen()
            print(f'Side A is listening to port {self.port}')
            side_b_socket, side_b_address = side_a_socket.accept()
            print(f'Side B connecting to port {self.port}')

            with side_b_socket:
                data = side_b_socket.recv(1024).decode()
                if data == 'exit':
                    print(f'Side B: {data}')
                    print('Carousel stopped')
                    return 'exit'

                print(f'Side B: {data}')
                new_port = int(data.split(' ')[-1])

            print('Side B disconnected')

        return new_port

    def __client_role(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as side_a_socket:
            side_a_socket.connect((self.ip, self.port))
            user_input = input('Enter message: ')
            # user_input = str(random.randint(1025, 65536))
            side_a_socket.send(user_input.encode())

            if user_input == 'exit':
                print('Carousel stopped')
                return 'exit'

            new_port = int(user_input.split(' ')[-1])

        return new_port

    def start_carousel(self):
        prev_port = self.port

        while True:
            if self.role == ServerClient.SERVER_ROLE:
                returned_value = self.__server_role()
                if returned_value == 'exit':
                    break

                self.port = returned_value
                self.role = ServerClient.CLIENT_ROLE

            if self.role == ServerClient.CLIENT_ROLE:
                returned_value = self.__client_role()
                if returned_value == 'exit':
                    break

                self.port = returned_value
                self.role = ServerClient.SERVER_ROLE

            if self.port == prev_port:
                print('Duplicate port detected. Exiting...')
                break

            prev_port = self.port
