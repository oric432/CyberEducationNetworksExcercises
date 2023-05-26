import socket
import protocol
from glob import glob
import os
import shutil
import subprocess
import pyautogui
import re
from dotenv import load_dotenv

load_dotenv()


SCREENSHOTS_PATH = os.environ['SCREENSHOTS_PATH']


def get_all_files(directory):
    return glob(os.path.join(directory, '*.*'))


def delete_file(path):
    if not os.path.exists(path):
        return 'File does not exist'
    try:
        os.remove(path)
        return 'File deleted successfully'
    except Exception as e:
        return e.__str__()


def copy_files(source, destination):
    if not os.path.exists(source) or not os.path.exists(destination):
        return 'One of files does not exist'
    try:
        shutil.copy(source, destination)
        return 'File copied successfully'
    except Exception as e:
        return e.__str__()


def execute_program(path):
    print(path)
    if not os.path.exists(path):
        return 'Path does not exist'
    try:
        subprocess.call(path)
        return 'Executed the program'
    except Exception as e:
        return e.__str__()


def get_screenshot_number(path):
    if os.path.exists(path):
        try:
            if len(os.listdir(path)) == 0:
                return -1
            return int(re.search(r'\w+_(\d+).png', sorted(glob(os.path.join(path, '*.png')))[-1]).group(1))
        except Exception as e:
            print(e.__str__())
    else:
        print('folder does not exist')


def take_screenshot():
    try:
        my_screenshot = pyautogui.screenshot()
        my_screenshot.save(os.path.join(SCREENSHOTS_PATH,
                                        f'screenshot_{get_screenshot_number(SCREENSHOTS_PATH) + 1}.png'))
        return 'Screenshot has been taken and saved to the server successfully'
    except Exception as e:
        return e.__str__()


def send_photo(client_socket):
    last_image = os.path.join(SCREENSHOTS_PATH,
                              f'screenshot_{get_screenshot_number(SCREENSHOTS_PATH)}.png')
    try:
        with open(last_image, 'rb') as img:
            client_socket.send(protocol.encode_photo(img.read()))
            print('Image sent successfully')
            return True, ''
    except FileNotFoundError as e:
        print(e.__str__())
        return False, 'File not found'


def get_server_response(cmd):
    command = cmd.split(' ')[0]
    args = re.findall(r"[A-Za-z]:\\(?:[A-Za-z0-9_\s]+\\)*[A-Za-z0-9_\s]*\.?[A-Za-z0-9_]*", cmd)
    if command == 'TAKE_SCREENSHOT':
        return take_screenshot()

    if not len(args):
        return 'Invalid file path'

    if command == 'DIR':
        return '\r\n\r\n'.join(get_all_files(args[0]))
    if command == 'DELETE':
        return delete_file(args[0])
    if command == 'COPY':
        return copy_files(args[0], args[1])
    if command == 'EXECUTE':
        return execute_program(args[0])
    return 'Invalid Command'


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((protocol.SERVER_IP, int(protocol.PORT)))
        server_socket.listen()
        print(f'Server is up and listening on port {protocol.PORT}')
        client_socket, client_address = server_socket.accept()
        print(f'Client {client_address} has connected')

        with client_socket:
            while True:
                is_valid_msg, msg = protocol.decode_message(client_socket)

                if is_valid_msg:
                    print('Client said: ' + msg)

                    if protocol.is_valid_command(msg):
                        if msg == 'SEND_PHOTO':
                            is_valid, err = send_photo(client_socket)
                            if is_valid:
                                continue
                            else:
                                response = err
                        else:
                            response = get_server_response(msg)
                    else:
                        response = 'Invalid Command'
                else:
                    response = 'Invalid Request' + msg

                if msg == 'EXIT':
                    break

                client_socket.send(protocol.encode_message(response).encode('utf-8').strip())


if __name__ == '__main__':
    main()
