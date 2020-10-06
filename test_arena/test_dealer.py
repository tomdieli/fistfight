import asyncio
from pywsitest import WSTest, WSResponse, WSMessage

from .fixtures import ws_test_client as test_client

async def do_user():
    await asyncio.sleep(0.5)

    ws_test = (
        WSTest("ws://127.0.0.1:8000/submit")
        .with_message(
            WSMessage()
            .with_attribute("type", "message")
            .with_attribute("action", "ping")
        )
    )
    await ws_test.run()
    assert ws_test.is_complete()


async def do_other_user():
    await asyncio.sleep(0.5)

    ws_test = (
        WSTest("ws://127.0.0.1:8000/receive")
        .with_response_timeout(0.5)
        .with_response(
            WSResponse()
            .with_attribute("type", "message")
            .with_attribute("action", "ping")
        )
    )
    await ws_test.run()
    assert ws_test.is_complete()

async def run_dos():
    await asyncio.gather(do_user(),do_other_user())

def test_dealer(test_client):
    asyncio.get_event_loop().run_until_complete(run_dos())

