# MindBot: Mind-Controlled Bracket Bot 

control a [BracketBot](https://www.bracket.bot/) using mental commands detected by the Emotiv EPOC X headset. streamed through emotiv's cortex API, and delivered via MQTT over wi-fi :)


---

## Requirements

- bracket bot
- emotiv developer account with API access (Pro or Pro Trial)
- emotiv EPOC X headset
- mosquitto broker installed and running on pi
- emotiv launcher + emotiv BCI installed and running on mac
- cortexService running on mac (check port 6868)

---


## Setup

note: go through [quickstart](https://github.com/BracketBotCapstone/quickstart) for bracket bot prior to following these instructions

### 1. Raspberry Pi Setup

- install Mosquitto MQTT broker:

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

- run the motor control script (`node_drive.py`) on Pi:

```bash
python3 node_drive.py
```

^ this listens for MQTT commands like `"forward"`, `"stop"`, etc.

### 2. Mac Setup

- clone repository locally
- install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Emotiv Setup

- connect EPOC X headset via Bluetooth in Emotiv Launcher
- create a trained profile with mental commands like "push" and "neutral"
- grant Cortex API access (should pop up when script requests access)

### 4. Running the System

- launch `node_eeg.py` on your mac

```bash
python3 mental_command_mqtt.py
```

this connects to Emotiv, streams mental commands, and publishes over MQTT

- press "push" mentally → **robot drives forward**
- relax to "neutral" → **robot stops**

---


## Troubleshooting (i've been through it all)

| Symptom | Fix |
|---------|-----|
| no headset detected in script | restart Emotiv Launcher and CortexService |
| no authorization popup | restart Launcher, check API access |
| "auth missing" error | you must have Emotiv Pro or Trial API access |
| "connection refused" on MQTT | fix Mosquitto config to listen globally |
| commands not moving robot | check ODrive connection and set_velocity() logs |

---

## Resources

- [Bracket Bot Quickstart Walkthrough](https://docs.bracket.bot/docs/kit-assembly)
- [Emotiv Cortex API Docs](https://emotiv.gitbook.io/cortex-api/)
- [Mosquitto MQTT Docs](https://mosquitto.org/)
- [ODrive Robotics](https://docs.odriverobotics.com/)

---

## Future Improvements

- add smoother mental command filtering (ignore low-power false positives) <- done via Emotiv, not repo-applicable
- add backward and turn mental commands
