# MindBot: Mind-Controlled Bracket Bot 

control a [bracket bot](https://www.bracket.bot/) using mental commands detected by the Emotiv EPOC X headset. streamed through emotiv's cortex API, and delivered via MQTT over wi-fi :)


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

- install mosquitto MQTT broker:

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

- run the motor control script (`node_drive.py`) on raspberry pi:

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

- connect EPOC X headset via bluetooth in emotiv launcher
- create a trained profile with mental commands like "push" and "neutral"
- grant cortex API access (should pop up when script requests access)

### 4. Running the System

- launch `node_eeg.py` on your mac

```bash
python3 node_eeg.py
```

this connects to emotiv, streams mental commands, and publishes over MQTT

- press "push" mentally → **robot drives forward**
- relax to "neutral" → **robot stops**

---


## Troubleshooting (i've been through it all)

| Symptom | Fix |
|---------|-----|
| no headset detected in script | restart emotiv launcher and cortexService |
| no authorization popup | restart launcher, check API access |
| "auth missing" error | you must have emotiv Pro or Trial API access |
| "connection refused" on MQTT | fix mosquitto config to listen globally |
| commands not moving robot | check odrive connection and set_velocity() logs |

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
