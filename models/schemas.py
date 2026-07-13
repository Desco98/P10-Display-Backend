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

class DeviceStatus(BaseModel):
    ip: str = ""
    sta_ip: str = "N/A"
    rssi: int = 0
    uptime: str = ""
    freeHeap: int = 0
    brightness: int = 0
    currentMessage: str = ""
    mode: str = "ap"
