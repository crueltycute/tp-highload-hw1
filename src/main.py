from config.config import Config
from handler.handler import Handler
from server.server import Server


# CONFIG_FILE_NAME = '../httpd.conf'
CONFIG_FILE_NAME = 'httpd.conf'


def main():
    config = Config()
    config.read(CONFIG_FILE_NAME)
    print(config)

    handler = Handler(config.document_root)

    server = Server(config, handler)
    try:
        server.launch()
        print(f'Server is launching on {config.host}:{config.port}')
    except KeyboardInterrupt:
        server.stop()
        print('Server stopped')


if __name__ == '__main__':
    main()
