class Request:
    def __init__(self, data, connection=''):
        request_data = data.split(b'\n')[0].split()

        if len(request_data) != 0:
            self.method = request_data[0]
            self.url = request_data[1].split(b'?')[0]
            self.protocol = request_data[2]
            self.connection = connection
        else:
            self.method = ''
            self.url = ''
            self.protocol = b''
            self.connection = 'close'

    @property
    def get_method(self):
        return self.method

    @property
    def get_url(self):
        return self.url

    @property
    def get_protocol(self):
        return self.protocol

    @property
    def get_connection(self):
        return self.connection
