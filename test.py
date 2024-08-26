import RPi.GPIO as GPIO
from services.device_measurements import DeviceMeasurements
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

deviceMeasurements = DeviceMeasurements()

while 1:
    GPIO.output(17, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    print(deviceMeasurements.getBatteryVoltage())
    time.sleep(1)
