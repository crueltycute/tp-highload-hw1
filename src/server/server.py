import asyncio
import uvloop
import os

from config.config import Config
from handler.handler import Handler


class Server:
    def __init__(self, config: Config, handler: Handler):
        self.config = config
        self.handler = handler
        self.loop = asyncio.get_event_loop()
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def start_coroutine(self, loop):
        await asyncio.start_server(client_connected_cb=self.handler.handle,
                                   host=self.config.host,
                                   port=self.config.port,
                                   loop=loop,
                                   reuse_port=True)

    def launch(self):
        processes = []

        for i in range(self.config.cpu_limit):
            process_id = os.fork()
            processes.append(process_id)

            if process_id == 0:
                for j in range(self.config.threads):
                    self.loop.create_task(self.start_coroutine(self.loop))
                try:
                    self.loop.run_forever()
                except KeyboardInterrupt:
                    self.stop()
                    print('Server stopped')
                finally:
                    print('Server is shutting down\n')

        print(f'Processes: {processes}')
        for p in processes:
            os.waitpid(p, 0)

    def stop(self):
        self.loop.stop()
