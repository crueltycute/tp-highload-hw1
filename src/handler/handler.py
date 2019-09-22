from asyncio import StreamReader, StreamWriter

from handler.executor import Executor
from handler.serializer import Serializer

from models.request import Request


CHUNK_SIZE = 1024


class Handler:
    def __init__(self, document_root):
        self.document_root = document_root
        self.executor = Executor(document_root)
        self.serializer = Serializer()

    async def handle(self, reader: StreamReader, writer: StreamWriter):
        data = b''

        while True:
            data += reader.read(CHUNK_SIZE)

            if not data or reader.at_eof() or data[-4:] == b'\r\n\r\n':
                break

        if len(data) > 0:
            request = Request(data)
            response_data = await self.executor.execute(request)
            response = await self.serializer.dump(response_data)
            writer.write(response)
            await writer.drain()
            writer.close()
