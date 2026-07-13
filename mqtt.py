import json
import asyncio
import aiomqtt
from core.config import settings
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# In-memory storage for device status
# Key: device_id, Value: dict of status
devices_state: Dict[str, Any] = {}

class MQTTClientManager:
    def __init__(self):
        self.client: aiomqtt.Client | None = None
        self._task: asyncio.Task | None = None

    async def start(self):
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self):
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _run_loop(self):
        tls_params = aiomqtt.TLSParameters() if settings.MQTT_USE_TLS else None
        
        while True:
            try:
                async with aiomqtt.Client(
                    hostname=settings.MQTT_BROKER,
                    port=settings.MQTT_PORT,
                    username=settings.MQTT_USERNAME,
                    password=settings.MQTT_PASSWORD,
                    tls_params=tls_params
                ) as client:
                    self.client = client
                    logger.info("Connected to MQTT Broker!")
                    
                    # Subscribe to all device status topics: p10/+/status
                    await client.subscribe("p10/+/status")
                    
                    async for message in client.messages:
                        topic = str(message.topic)
                        payload = message.payload.decode()
                        
                        try:
                            # Parse p10/{device_id}/status
                            parts = topic.split('/')
                            if len(parts) == 3 and parts[2] == 'status':
                                device_id = parts[1]
                                data = json.loads(payload)
                                devices_state[device_id] = data
                                logger.debug(f"Updated status for {device_id}: {data}")
                        except Exception as e:
                            logger.error(f"Error parsing MQTT message on {topic}: {e}")
                            
            except aiomqtt.MqttError as error:
                logger.error(f"MQTT connection error: {error}. Reconnecting in 5 seconds...")
                self.client = None
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                logger.info("MQTT Client stopped.")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}. Reconnecting in 5 seconds...")
                self.client = None
                await asyncio.sleep(5)

    async def publish_message(self, topic: str, payload: Dict | str) -> bool:
        if not self.client:
            logger.warning("MQTT client not connected, message not sent.")
            return False
            
        try:
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            await self.client.publish(topic, payload)
            return True
        except Exception as e:
            logger.error(f"Failed to publish to {topic}: {e}")
            return False

mqtt_manager = MQTTClientManager()
