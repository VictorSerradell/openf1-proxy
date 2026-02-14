# archivo: models/schemas.py
from pydantic import BaseModel
from typing import Any, List, Dict


class DriverTelemetryResponse(BaseModel):
    driver_number: int
    car_data: List[Dict[str, Any]]
    position: List[Dict[str, Any]]
    laps: List[Dict[str, Any]]
    intervals: List[Dict[str, Any]]
