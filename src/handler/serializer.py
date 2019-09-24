class Serializer:
    def __init__(self):
        pass

    @staticmethod
    async def dump(response):
        # print(f'Response: {response.status}\n')
        if response.status == '200 OK':
            return Serializer.good_resp(response).encode() + response.body
        else:
            return Serializer.bad_resp(response).encode()

    @staticmethod
    def good_resp(response):
        return f'{response.protocol} {response.status}\r\n' \
               f'Server: {response.server}\r\n' \
               f'Date: {response.date}\r\n' \
               f'Connection: {response.connection}\r\n' \
               f'Content-Length: {response.content_length}\r\n' \
               f'Content-Type: {response.content_type}\r\n\r\n'

    @staticmethod
    def bad_resp(response):
        return f'{response.protocol} {response.status}\r\n' \
               f'Server: {response.server}\r\n' \
               f'Date: {response.date}\r\n' \
               f'Connection: {response.connection}\r\n\r\n'
