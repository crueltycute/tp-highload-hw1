import asyncio
import uvloop
import os

from config.config import Config
from handler.handler import Handler


class Server:
    def __init__(self, config: Config, handler: Handler):
        self.config = config
        self.loop = None
        self.handler = handler

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def start_subserver(self, loop):
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
                self.loop = asyncio.get_event_loop()
                self.loop.create_task(self.start_subserver(self.loop))
                self.loop.run_forever()

        print(f'Number of launched subservers: {len(processes)}')
        print(f'Subservers PID: {processes}')

        for p in processes:
            os.waitpid(p, 0)

    def stop(self):
        if not self.loop is None:
            self.loop.stop()
