from pydantic import BaseModel, Field

class MessagePayload(BaseModel):
    device_id: str
    content: str
    animation: str = "scroll"
    fontStyle: str = "normal"
    fontSize: int = 2

class BrightnessPayload(BaseModel):
    device_id: str
    level: int = Field(..., ge=0, le=100)

from typing import Optional

class DeviceStatus(BaseModel):
    ip: Optional[str] = ""
    sta_ip: Optional[str] = "N/A"
    rssi: Optional[int] = 0
    uptime: Optional[str] = ""
    freeHeap: Optional[int] = 0
    brightness: Optional[int] = 0
    currentMessage: Optional[str] = ""
    mode: Optional[str] = "ap"
