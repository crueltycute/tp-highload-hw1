DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = '80'
DEFAULT_CPU_LIMIT = 4
DEFAULT_THREADS = 2
DEFAULT_DOC_ROOT = '/var/www/html'


class Config:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT,
                 cpu_limit=DEFAULT_CPU_LIMIT, threads=DEFAULT_THREADS,
                 document_root=DEFAULT_DOC_ROOT):
        self.host = host
        self.port = port
        self.cpu_limit = cpu_limit
        self.threads = threads
        self.document_root = document_root

    def read(self, file_name):
        config_data = {}

        with open(file_name, 'r') as config_file:
            for line in config_file:
                key, value = line.strip().split(' ')
                config_data.update({key: value})

            if config_data.get('host') is None:
                self.host = DEFAULT_HOST
            else:
                self.host = config_data['host']

            if config_data.get('port') is None:
                self.port = DEFAULT_PORT
            else:
                self.port = config_data['port']

            if config_data.get('cpu_limit') is None:
                self.cpu_limit = DEFAULT_CPU_LIMIT
            else:
                self.cpu_limit = int(config_data['cpu_limit'])

            if config_data.get('thread_limit') is None:
                self.threads = DEFAULT_THREADS
            else:
                self.threads = int(config_data['thread_limit'])

            if config_data.get('document_root') is None:
                self.document_root = DEFAULT_DOC_ROOT
            else:
                self.document_root = config_data['document_root']

        print(f'\nConfig read from file: {file_name}\n')

    def __str__(self):
        return (f'host: {self.host} \n'
              f'port: {self.port} \n'
              f'cpu limit: {self.cpu_limit}\n'
              f'threads: {self.threads}\n'
              f'document_root: {self.document_root}\n')
