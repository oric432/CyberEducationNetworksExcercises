import socket
import protocol
import os
from dotenv import load_dotenv

load_dotenv()


IP = os.environ['CLIENT_IP']


def get_photo(client_socket):
    is_valid_res, res = protocol.decode_photo(client_socket)
    if is_valid_res:
        with open('Screenshot.jpg', 'wb') as empty_img:
            empty_img.write(res)
            print('Image transferred successfully')
    else:
        print('invalid server response: ' + res)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((IP, int(protocol.PORT)))

        while True:
            user_input = input('Enter a command: ')

            if protocol.is_valid_command(user_input):
                encoded_msg = protocol.encode_message(user_input)
                client_socket.send(encoded_msg.encode('utf-8').strip())

                if user_input == 'EXIT':
                    print('BYE BYE')
                    break

                if user_input == 'SEND_PHOTO':
                    get_photo(client_socket)
                else:
                    is_valid_res, res = protocol.decode_message(client_socket)
                    if is_valid_res:
                        print('Server sent: ' + res)
                    else:
                        print('invalid server response: ' + res)
            else:
                print('invalid user command')


if __name__ == '__main__':
    main()
