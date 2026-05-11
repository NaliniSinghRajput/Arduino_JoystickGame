# Arduino Joystick Spaceship Game

This is a Python Pygame spaceship shooter game controlled using an Arduino Micro and a joystick module.

## Features

- Arduino joystick controls spaceship movement
- Joystick button fires bullets
- Enemy balls/asteroids fall from the top
- Player can shoot and destroy enemies
- Score and lives system

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
| VRx | A0 |
| VRy | A1 |
| SW | D2 |

## Python Libraries Required

Install the required libraries:

```bash
pip install -r requirements.txt