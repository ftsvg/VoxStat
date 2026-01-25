import asyncio
import uuid
import json

from websockets import connect

from config import Settings
from logger import logger


async def send_webhook_message(
    payload_type: str,
    payload_content: str,
    expect_response: bool = False,
    timeout: float = 3.0
) -> dict | None:

    payload = {
        "type": payload_type,
        "payload": {
            "message": payload_content
        }
    }

    try:
        async with connect(Settings.WEBSOCKET_URI) as websocket:
            await websocket.send(json.dumps(payload))

            if not expect_response:
                return None

            try:
                response = await asyncio.wait_for(
                    websocket.recv(),
                    timeout=timeout
                )
                return json.loads(response)

            except asyncio.TimeoutError:
                return None

    except Exception as error:
        logger.error(f"WebSocket error: {error}")
        return None