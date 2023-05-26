from dotenv import load_dotenv
import os

load_dotenv()

LENGTH_FIELD_SIZE = 4
PORT = os.environ['PORT']
COMMANDS = ['TIME', 'WHORU', 'RAND', 'EXIT']


def check_cmd(data):
    return data in COMMANDS


def create_msg(data):
    return str(len(data)).zfill(LENGTH_FIELD_SIZE) + data


def get_msg(my_socket):
    try:
        length = int(my_socket.recv(LENGTH_FIELD_SIZE).decode())
        message = my_socket.recv(length).decode()
        return True, message
    except ValueError as e:
        return False, e
    except Exception as e:
        return False, e
