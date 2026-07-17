from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from models.schemas import DeviceStatus, MessagePayload, BrightnessPayload
from mqtt import mqtt_manager, devices_state

router = APIRouter(prefix="/api/v1")

@router.get("/devices", response_model=Dict[str, Any])
async def list_devices():
    return devices_state

@router.get("/devices/{device_id}/status", response_model=DeviceStatus)
async def get_device_status(device_id: str):
    status = devices_state.get(device_id)
    if not status:
        raise HTTPException(status_code=404, detail="Device not found")
    return status

@router.post("/send")
async def send_message(payload: MessagePayload):
    topic = f"p10/{payload.device_id}/command/message"
    
    # Map the app's payload keys to the firmware's expected keys
    mqtt_payload = {
        "msg": payload.content,
        "anim": payload.animation,
        "font": payload.fontStyle,
        "size": payload.fontSize
    }
    
    success = await mqtt_manager.publish_message(topic, mqtt_payload)
    if not success:
        raise HTTPException(status_code=503, detail="Failed to send message via MQTT")
    return {"status": "success", "message": "Message sent"}

@router.post("/brightness")
async def set_brightness(payload: BrightnessPayload):
    topic = f"p10/{payload.device_id}/command/brightness"
    success = await mqtt_manager.publish_message(topic, {"level": payload.level})
    if not success:
        raise HTTPException(status_code=503, detail="Failed to send brightness command via MQTT")
    return {"status": "success", "message": "Brightness command sent"}

@router.get('/ping-server')
async def ping_render_server():
    return True