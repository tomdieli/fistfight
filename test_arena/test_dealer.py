import json
import asyncio
from subprocess import Popen, PIPE

import websockets

# from .fixtures import ws_test_client as test_client


async def sender():
    await asyncio.sleep(1.5)
    test_data = {"type": "message", "message": "Hello, there!"}
    send_url = "ws://127.0.0.1:5000/testor/submit"
    async with websockets.connect(send_url) as websocket:
        await websocket.send(json.dumps(test_data))
    print("SENT!")
    print(test_data)
    recv_url = "ws://127.0.0.1:5000/testor/receive"
    async with websockets.connect(recv_url) as websocket:
        response_string = await websocket.recv()      # (json.dumps(test_data))
        print(json.loads(response_string))

async def gedder():
    # await asyncio.sleep(0.5)
    recv_url = "ws://127.0.0.1:5000/testor/receive"
    async with websockets.connect(recv_url) as websocket:
        response_string = await websocket.recv()      # (json.dumps(test_data))
        print(json.loads(response_string))
        # await asyncio.sleep(0.5)


def test_dealer():
    gunicorn_pid = Popen(['gunicorn',
                            '-k', 'flask_sockets.worker',
                            '-b', '127.0.0.1:5000',
                            'arena:create_app()'])
    
    asyncio.get_event_loop().run_until_complete(sender())
    # print("SENT!")
    # asyncio.get_event_loop().run_until_complete(gedder())
    gunicorn_pid.terminate()

