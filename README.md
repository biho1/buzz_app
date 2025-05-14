# Project Title

webserver to use you smartphones as buzz input devices for PCSX2 and BUZZ games

## Description

An in-depth paragraph about your project and overview of use.

## Getting Started

### Dependencies

* python 3

### Executing program (for macOS)

cd Downloads/buzz_app 

export PATH="$(brew --prefix python)/libexec/bin:$PATH"

python -m venv ./env

source ./env/bin/activate

pip install flask pyautogui pyobjc-core pyobjc

python buzz_controller.py

* you need to grant access in accessibility control for terminal (system permission will be asked, to simulate key press events)

### Executing release version (for macOS)

alternatively you can download the compiled release version an run it directly from macos without installing python

* you need to have Sequoia installed
* you need to allow the unsigned app to run, in system settings > data and security -> scoll down to the bottom, after the first start it will be visible and you can allow execute
* you need to grant access for Buzz Controller in accessibility control (system permission will be asked, to simulate key press events)
 
## Help

keymapping has to be setup in PCSX2 fot the buzzers

Player 1: {'big': '1', 'blue': 'q', 'orange': 'w', 'green': 'e', 'yellow': 'r'}

Player 2: {'big': '2', 'blue': 'a', 'orange': 's', 'green': 'd', 'yellow': 'f'}

Player 3: {'big': '3', 'blue': 'z', 'orange': 'x', 'green': 'c', 'yellow': 'v'}

Player 4: {'big': '4', 'blue': 'u', 'orange': 'i', 'green': 'o', 'yellow': 'p'}

werbserver runs on port 80 so you can directly open http://yourip/ 

if you have to change this you have to edit buzz_controller.py at the bottom (2 places for change the port)

each players phone hat to be in the same WIFI and this python script hat to run on the machine that runs PCSX2

![Alt text](sample.jpeg "sample")

## Authors
chatGPT helped a lot
