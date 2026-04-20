import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led=26
GPIO.setup(led, GPIO.OUT)
divider = 6
GPIO.setup(divider, GPIO.IN)

while True:
    sensor_state = GPIO.input(divider)
    led_state = not sensor_state
    GPIO.output(led, led_state) 