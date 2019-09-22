from datetime import datetime


class Response:
    def __init__(self, status, protocol, connection, content_type='', content_length=0, body=b''):
        self.status = status
        self.protocol = protocol.decode()
        self.connection = connection
        self.content_type = content_type
        self.content_length = content_length
        self.body = body
        self.server = 'server'
        self.date = datetime.today()

    @property
    def get_status(self):
        return self.status

    @property
    def get_protocol(self):
        return self.protocol

    @property
    def get_connection(self):
        return self.content_type

    @property
    def get_content_length(self):
        return self.content_length
