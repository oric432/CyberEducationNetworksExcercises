from server_client import ServerClient
from dotenv import load_dotenv
import os

load_dotenv()
IP = os.environ['IP']
START_PORT = os.environ['PORT']


def main():
    my_side = ServerClient(ServerClient.CLIENT_ROLE, int(START_PORT), IP)

    my_side.start_carousel()


if __name__ == '__main__':
    main()
