#!/usr/bin/env python3

import json
import sys, os, asyncio, threading
from cortex import Cortex

CLIENT_ID = "client_id"  # replace with ID
CLIENT_SECRET = "client_secret"  # replace with secret

class MCListener(Cortex):
    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret, debug_mode=False)
        self.session_id = None
        self.bind(create_session_done=self.on_session)
        self.bind(new_com_data=self.on_com)

    def on_session(self, *args, **kwargs):
        self.session_id = kwargs.get("data")
        self.setup_profile("Amit-BB", status="load")
        self.set_mental_command_active_action(["neutral", "push", "pull", "left", "right"])  # adjust to specific commands you have trained!
        self.sub_request(["com"])

    def on_com(self, *args, **kwargs):
        print("👀 on_com triggered")
        print(kwargs)
        data = kwargs.get("data")
        if data:
            action = data[0]["action"]
            power = data[0]["power"]
            print(f"{action.upper()} ({power:.2f})")
        
    def control_device(self, command, headset_id=None):
        request = {
            "jsonrpc": "2.0",
            "id": 99,  # any unique ID
            "method": "controlDevice",
            "params": {
                "command": command
            }
        }
        if headset_id:
            request["params"]["headset"] = headset_id
        self.ws.send(json.dumps(request))


async def main():
    listener = MCListener(CLIENT_ID, CLIENT_SECRET)
    threading.Thread(target=listener.open, daemon=True).start()
    await asyncio.sleep(1)

    listener.request_access()
    await asyncio.sleep(2)
    listener.authorize()
    await asyncio.sleep(1)
    listener.query_headset()
    await asyncio.sleep(1)

    if listener.headset_id:
        listener.control_device("connect", listener.headset_id)
        await asyncio.sleep(1)
        listener.create_session()
    else:
        print("❌ no headset found.")
        return

    print("listening for mental commands. press ctrl + c to exit.")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        listener.close()

if __name__ == "__main__":
    asyncio.run(main())
