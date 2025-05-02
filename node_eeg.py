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
MQTT_BROKER_ADDRESS = "192.168.0.168"  # raspberry Pi's IP address
MQTT_TOPIC = "robot/drive"

PROFILE_NAME = "profile"  # trained profile
WANTED_HEADSET_ID = "EPOCX-X#######X"  # OPTIONAL: specify headset ID to use. if empty, it will use the first available.

CLIENT_ID = "client_id"  # replace with ID
CLIENT_SECRET = "client_secret"  # replace with secret

# ------------------------------------------------------------------------------------
# Setup MQTT
# ------------------------------------------------------------------------------------
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER_ADDRESS)
mqtt_client.loop_start()

# ------------------------------------------------------------------------------------
# Cortex Brain class
# ------------------------------------------------------------------------------------
class MCListener(Cortex):
    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret, debug_mode=False)
        self.session_id = None
        self.set_wanted_headset(WANTED_HEADSET_ID)
        self.set_wanted_profile(PROFILE_NAME)
        self.bind(create_session_done=self.on_session)
        self.bind(load_unload_profile_done=self.on_profile_loaded)
        self.bind(new_com_data=self.on_com)

    def on_session(self, *args, **kwargs):
        self.session_id = kwargs.get("data")
        self.setup_profile(PROFILE_NAME, status="load")

    def on_profile_loaded(self, *args, **kwargs):
        self.set_mental_command_active_action(["neutral", "push"])
        self.sub_request(["com"])

    def on_com(self, *args, **kwargs):
        data = kwargs.get("data")
        if data:
            action = data["action"]
            power = data["power"]
            print(f"{action.upper()} ({power:.2f})")
            if action == "push":
                print("SENDING: forward")
                mqtt_client.publish(MQTT_TOPIC, "forward")
            elif action == "neutral":
                print("SENDING: stop")
                mqtt_client.publish(MQTT_TOPIC, "stop")
            else:
                print("unexpected action")

# ------------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------------
async def main():
    listener = MCListener(CLIENT_ID, CLIENT_SECRET)
    threading.Thread(target=listener.open, daemon=True).start()
    await asyncio.sleep(1)

    listener.request_access()
    await asyncio.sleep(2)
    listener.authorize()
    await asyncio.sleep(2)

    for _ in range(10):
        listener.query_headset()
        await asyncio.sleep(1)
        if listener.headset_id and listener.isHeadsetConnected:
            break

    if not listener.headset_id or not listener.isHeadsetConnected:
        print("❌ no headset connected.")
        return

    listener.control_device("connect", listener.headset_id)
    await asyncio.sleep(2)
    listener.create_session()
    await asyncio.sleep(2)

    print("listening for mental commands. press ctrl + c to exit.")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        listener.close()
        mqtt_client.loop_stop()

# ------------------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
