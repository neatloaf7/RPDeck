# RPdeck
## An RP2040 based volume controller for windows

WORK IN PROGRESS

### Project description
A Volume controller for windows based around an RP2040. Features per application volume control and OLED Display support.
Firmware is written in CircuitPython. The RPDeck communicates with the host application over serial to send application switch and volume change commands, and receives information about the currently selected application and its volume

### Features to consider
Currently using soundswitch hotkeyed to F13 to switch output device, I will see if I can incorporate it into the host application.
Only 5 screen states: Spotify, Discord, Game, Master Volume, and Current Window. I will see if it is practical to display entire application names when game or current window is selected. I should add a screen state for internet browsers and for adding new applications that need a discrete screen state.

### Notes
CircuitPython 9.2.4 broke the functionality of rotaryio so I am currently using CircuitPython 9.2.1. I believe this was fixed by https://github.com/adafruit/circuitpython/pull/10025. I have yet to test any newer releases.
