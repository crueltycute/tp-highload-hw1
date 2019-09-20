from config import Config


CONFIG_FILE_NAME = '../httpd.conf'


def main():
    config = Config()
    config.read(CONFIG_FILE_NAME)
    print(config)


if __name__ == '__main__':
    main()
