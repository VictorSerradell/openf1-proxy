# archivo: routers/openf1.py
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from typing import Any, Dict
from services.openf1_service import service
from config import settings
from models.schemas import DriverTelemetryResponse
from utils.rate_limit import limiter


router = APIRouter(prefix="/f1", tags=["OpenF1"])


def verify_api_key(request: Request):
    key = request.headers.get("X-API-Key")
    if settings.api_keys_list and key not in settings.api_keys_list:
        raise HTTPException(status_code=401, detail="Invalid API Key")


@router.get("/{endpoint}")
@limiter.limit("10/second")
async def proxy_endpoint(
    request: Request,
    endpoint: str,
    format: str = Query(default="json"),
    _: Any = Depends(verify_api_key),
):
    ttl = settings.CACHE_LIVE_TTL
    params = dict(request.query_params)
    data = await service.fetch(endpoint, params, ttl)

    if format == "csv":
        return PlainTextResponse(str(data))

    return JSONResponse(content=data)


@router.get("/latest-session")
async def latest_session():
    sessions = await service.fetch("sessions", {}, settings.CACHE_LIVE_TTL)
    if not sessions:
        raise HTTPException(status_code=404, detail="No sessions found")
    return sessions[0]


@router.get(
    "/driver-telemetry/{driver_number}",
    response_model=DriverTelemetryResponse,
)
async def driver_telemetry(driver_number: int, request: Request):
    params = dict(request.query_params)
    params["driver_number"] = driver_number

    car_data = await service.fetch("car_data", params, settings.CACHE_LIVE_TTL)
    position = await service.fetch("position", params, settings.CACHE_LIVE_TTL)
    laps = await service.fetch("laps", params, settings.CACHE_LIVE_TTL)
    intervals = await service.fetch("intervals", params, settings.CACHE_LIVE_TTL)

    return DriverTelemetryResponse(
        driver_number=driver_number,
        car_data=car_data,
        position=position,
        laps=laps,
        intervals=intervals,
    )
