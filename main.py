# Trinket IO demo
# Welcome to CircuitPython 3.1.1 :)

import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogOut, AnalogIn
import adafruit_dotstar as dotstar
import time
from pulseio import PWMOut

# One pixel connected internally!
#dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.3)

# Built in red LED
#led = DigitalInOut(board.D13)
#led.direction = Direction.OUTPUT

# Analog input on D0
photocell = AnalogIn(board.A4)

# Analog output on D1
display = PWMOut(board.A2)

# Digital input with pullup on D2
increment_button = DigitalInOut(board.D2)
increment_button.direction = Direction.INPUT
increment_button.pull = Pull.UP

# Capacitive touch on D3
decrement_button = DigitalInOut(board.D3)
decrement_button.direction = Direction.INPUT
decrement_button.pull = Pull.UP

# NeoPixel strip (of 16 LEDs) connected on D4
#NUMPIXELS = 16
#neopixels = neopixel.NeoPixel(board.D4, NUMPIXELS, brightness=0, auto_write=False)

led = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.1)
led[0] = (0, 0, 0)


######################### HELPERS ##############################


######################### MAIN LOOP ##############################

prev_increment_state = False
prev_decrement_state = False
tint = 100
offset = 0
while True:
  print((tint, offset))
  # Read analog voltage on D0
  light_intensity = int(round(photocell.value / 256))

  increment_state = increment_button.value
  if increment_state != prev_increment_state:
      if increment_state:
        print("Button on D2 pressed!")
        offset += 10

  decrement_state = decrement_button.value
  if decrement_state != prev_decrement_state:
      if decrement_state:
        print("Button on D3 pressed!")
        offset -= 10

  tint = light_intensity + offset

  if tint > 255:
    offset = 255 - light_intensity
  elif tint < 0:
    offset = -1 * light_intensity

  tint = light_intensity + offset

  prev_increment_state = increment_state
  prev_decrement_state = decrement_state

  # set analog output to 0-3.3V (0-65535 in increments)

  display.duty_cycle = tint * 256
  print(display.duty_cycle)

  time.sleep(0.1) # make bigger to slow down
