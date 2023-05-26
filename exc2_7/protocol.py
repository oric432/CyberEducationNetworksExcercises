import re
from dotenv import load_dotenv
import os

load_dotenv()

SERVER_IP = '0.0.0.0'
PORT = os.environ['PORT']
LENGTH_FIELD_SIZE = 4
COMMANDS = ['DIR', 'DELETE', 'COPY', 'EXECUTE', 'TAKE_SCREENSHOT', "EXIT", 'SEND_PHOTO']


def is_valid_command(cmd):
    return bool([command for command in COMMANDS
                if re.match(command, cmd)])


def encode_message(data):
    return str(len(data)).zfill(LENGTH_FIELD_SIZE) + data


def encode_photo(image):
    image_bytes_len = len(image)
    image_bytes_len_len = len(str(image_bytes_len))
    return (str(image_bytes_len_len).zfill(LENGTH_FIELD_SIZE) + str(image_bytes_len)).encode() + image


def decode_photo(socket):
    try:
        image_bytes_len_len = socket.recv(LENGTH_FIELD_SIZE).decode()
        image_bytes_len = socket.recv(int(image_bytes_len_len)).decode()
        image_bytes = socket.recv(int(image_bytes_len))
        return True, image_bytes
    except ValueError as e:
        return False, e.__str__()
    except Exception as e:
        return False, e.__str__()


def decode_message(socket):
    try:
        length = socket.recv(LENGTH_FIELD_SIZE).decode()
        data = socket.recv(int(length)).decode()
        return True, data
    except ValueError as e:
        return False, e.__str__()
    except Exception as e:
        return False, e.__str__()
