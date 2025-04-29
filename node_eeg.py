#!/usr/bin/env python3

import sys
import os
import asyncio
import json
import ssl
import paho.mqtt.client as mqtt

from cortex import Cortex

# ------------------------------------------------------------------------------------
# Config
# ------------------------------------------------------------------------------------
PROFILE_NAME = "profile"  # trained profile
MQTT_BROKER_ADDRESS = "192.168.0.168"  # Raspberry Pi's IP address
MQTT_TOPIC = "robot/drive"

CORTEX_CREDS = {
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "license": "",
    "debit": 100
}

# ------------------------------------------------------------------------------------
# Setup MQTT
# ------------------------------------------------------------------------------------
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER_ADDRESS)
mqtt_client.loop_start()

# ------------------------------------------------------------------------------------
# Cortex Brain class
# ------------------------------------------------------------------------------------
class BracketBotBrain(Cortex):
    async def on_mental_command(self, *args, **kwargs):
        action = kwargs['data'][0]['action']
        power = kwargs['data'][0]['power']
        print(f"[EEG] Command Detected: {action} (Power: {power:.2f})")

        if action == "push":
            print("Sending: forward")
            mqtt_client.publish(MQTT_TOPIC, "forward")
        elif action == "neutral":
            print("Sending: stop")
            mqtt_client.publish(MQTT_TOPIC, "stop")

# ------------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------------
async def main():
    bot_brain = BracketBotBrain(
        client_id=CORTEX_CREDS["client_id"],
        client_secret=CORTEX_CREDS["client_secret"],
        license=CORTEX_CREDS["license"],
        debit=CORTEX_CREDS["debit"]
    )

    bot_brain.open()
    await bot_brain.request_access()
    await bot_brain.authorize()
    await bot_brain.query_headsets()
    await bot_brain.setup_profile(PROFILE_NAME, status="load")
    await bot_brain.start(["mentalCommand"])

    print("Streaming mental commands to MQTT!")
    
    while True:
        await asyncio.sleep(1)

# ------------------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping stream...")
        mqtt_client.publish(MQTT_TOPIC, "stop")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
