import socket
import protocol
from dotenv import load_dotenv
import os

load_dotenv()

IP = os.environ['IP']


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
        my_socket.connect((IP, protocol.PORT))

        while True:
            user_input = input("Enter command\n")

            if protocol.check_cmd(user_input):
                new_input = protocol.create_msg(user_input)
                my_socket.send(new_input.encode())

                if user_input == 'EXIT':
                    break

                is_valid, response = protocol.get_msg(my_socket)

                if is_valid:
                    print(response)
                else:
                    print("Response not valid\n", response)
            else:
                print("Not a valid command")


if __name__ == "__main__":
    main()
