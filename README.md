# Arduino Joystick Spaceship Game

YouTube Link:- https://youtube.com/shorts/iNRXAMAtdqs?si=A-hCTBiTjOtwQHs1

This is a Python spaceship shooter game controlled using an Arduino Micro and a joystick module.

## Features

- Move spaceship using joystick
- Shoot bullets using joystick button
- Enemy balls/asteroids fall from the top
- Score and lives system
- Built using Python, Pygame, PySerial, and Arduino

## Hardware Required

- Arduino Micro
- Joystick module
- USB cable
- Computer with Python installed

## Joystick Connections

| Joystick Pin | Arduino Micro |
|---|---|
| VCC | 5V |
| GND | GND |
| VRx / X | A0 |
| VRy / Y | A1 |
| SW / Button | D2 |

## Python Libraries Required

Install the required libraries using:

```bash
pip install -r requirements.txt
```

## How to Run

First, close the Arduino Serial Monitor.

Then run:

```bash
python spaceship_game.py
```

## Important

Change the COM port in the Python file if required:

```python
PORT = "COM3"
```

For example, if your Arduino is on COM4, change it to:

```python
PORT = "COM4"
```

## Project Files

- `spaceship_game.py` - Main game file
- `requirements.txt` - Required Python libraries
- `.gitignore` - Files and folders ignored by Git
