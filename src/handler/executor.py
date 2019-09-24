import os
import aiofiles
import urllib.parse

from models.response import Response


ALLOWED_METHODS = {
    'GET': b'GET',
    'HEAD': b'HEAD'
}

ALLOWED_CODES = {
    200: '200 OK',
    403: '403 Forbidden',
    404: '404 Not Found',
    405: '405 Method Not Allowed',
}

ALLOWED_CONTENT_TYPES = {
    'html': 'text/html',
    'css': 'text/css',
    'js': 'application/javascript',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'swf': 'application/x-shockwave-flash',
    'txt': 'text/txt',
    'default': 'text/plain'
}


class Executor:
    def __init__(self, document_root):
        self.document_root = document_root

    async def execute(self, request):
        if request.get_method == ALLOWED_METHODS.get('HEAD'):
            # print('Request: HEAD')
            return await self.execute_head(request)
        elif request.get_method == ALLOWED_METHODS.get('GET'):
            # print('Request: GET')
            return await self.execute_get(request)
        else:
            # print('Request: Unknown')
            return Response(ALLOWED_CODES.get(405), request.get_protocol, request.get_connection)

    async def execute_head(self, request):
        file_data = self.get_file_info(request)

        if file_data == 403:  # forbidden error
            return Response(status=ALLOWED_CODES.get(403), protocol=request.protocol, connection='')
        elif file_data == 404:  # not found error
            return Response(status=ALLOWED_CODES.get(404), protocol=request.protocol, connection='')
        else:
            return Response(status=ALLOWED_CODES.get(200), protocol=request.protocol, connection='closed',
                            content_length=file_data.get('content_length'), content_type=file_data.get('content_type'))

    async def execute_get(self, request):
        file_data = self.get_file_info(request)

        if file_data == 403:  # forbidden error
            return Response(status=ALLOWED_CODES.get(403), protocol=request.protocol, connection='')
        elif file_data == 404:  # not found error
            return Response(status=ALLOWED_CODES.get(404), protocol=request.protocol, connection='')
        else:
            body = await self.read_file(file_data.get('file_name'))
            return Response(status=ALLOWED_CODES.get(200), protocol=request.protocol, connection='closed',
                            content_length=file_data.get('content_length'), content_type=file_data.get('content_type'),
                            body=body)

    def get_file_info(self, request):
        file_path = request.get_url.decode()
        file_path = urllib.parse.unquote(file_path, encoding='utf-8', errors='replace')
        if len(file_path.split('../')) > 1:
            return 403

        if file_path[-1:] == '/':
            file = self.document_root + file_path + 'index.html'
        else:
            file = self.document_root + file_path

        if file.split('.')[-1:][0] in ALLOWED_CONTENT_TYPES:
            content = ALLOWED_CONTENT_TYPES[file.split('.')[-1]]
        else:
            content = ''

        if not os.path.isfile(file):
            if file_path[-1:] == '/' and file_path.count('.') < 1:
                return 403
            else:
                return 404

        return {'file_name': file,
                'file_path': file_path,
                'content_type': content,
                'content_length': os.path.getsize(file)}

    @staticmethod
    async def read_file(filename):
        async with aiofiles.open(filename, mode='rb') as file:
            return await file.read()
