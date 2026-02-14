# archivo: routers/ws.py
from fastapi import APIRouter, WebSocket
from services.openf1_service import service
import asyncio

router = APIRouter()

@router.websocket("/ws/telemetry/{driver_number}")
async def websocket_telemetry(websocket: WebSocket, driver_number: int):
    await websocket.accept()

    try:
        while True:
            data = await service.fetch(
                "car_data",
                {"driver_number": driver_number},
                ttl=5,
            )
            await websocket.send_json(data)
            await asyncio.sleep(2)

    except Exception:
        await websocket.close()
