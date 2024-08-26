import RPi.GPIO as GPIO
import time
import minimalmodbus
import smbus
from ina219 import INA219
import logging

class DeviceMeasurements:
    ina = INA219(shunt_ohms=0.1, max_expected_amps=0.6, address=0x40)
    ina.configure(voltage_range=ina.RANGE_16V, gain=ina.GAIN_AUTO)

    ina2 = INA219(shunt_ohms=0.1, max_expected_amps=0.6, address=0x41)
    ina2.configure(voltage_range=ina.RANGE_16V, gain=ina.GAIN_AUTO)

    bus = smbus.SMBus(1)
    time.sleep(1)
    adc_address = 0x48
    battery_input = 0x42
    RELAY_IN = [4, 17, 27, 22, 18, 23, 24, 25]
    s1 = RELAY_IN[0]
    s2 = RELAY_IN[1]
    s3 = RELAY_IN[2]
    s4 = RELAY_IN[3]
    s5 = RELAY_IN[4]
    s6 = RELAY_IN[5]
    s7 = RELAY_IN[6]
    s8 = RELAY_IN[7]

    GPIO.setmode(GPIO.BCM)
    for relay in RELAY_IN:
        GPIO.setup(relay, GPIO.OUT)

    def batteryChargingMode(self, curr_time_slot):
        if 3 <= curr_time_slot <= 8:
            GPIO.output(self.s1, GPIO.LOW)
            GPIO.output(self.s4, GPIO.HIGH)
        else:
            GPIO.output(self.s4, GPIO.LOW)
            GPIO.output(self.s1, GPIO.HIGH)
            GPIO.output(self.s2, GPIO.LOW)
            GPIO.output(self.s7, GPIO.LOW)
            GPIO.output(self.s8, GPIO.LOW)
            GPIO.output(self.s3, GPIO.HIGH)
            GPIO.output(self.s5, GPIO.HIGH)
            GPIO.output(self.s6, GPIO.HIGH)

    def batteryDischargingMode(self):
        GPIO.output(self.s1, GPIO.LOW)
        GPIO.output(self.s4, GPIO.LOW)
        GPIO.output(self.s5, GPIO.LOW)
        GPIO.output(self.s6, GPIO.LOW)
        GPIO.output(self.s2, GPIO.HIGH)
        GPIO.output(self.s3, GPIO.HIGH)
        GPIO.output(self.s7, GPIO.HIGH)
        GPIO.output(self.s8, GPIO.HIGH)

    def readEM2M3Values(self):
        try:
            modbusAddress = [
                {"address": 100, "name": "Total Active Energy (kWh)", "f": 1},
                {"address": 102, "name": "Import Active Energy (kWh)", "f": 1},
                {"address": 104, "name": "Export Active Energy (kWh)", "f": 1},
                {"address": 106, "name": "Total Reactive Energy (kVArh)", "f": 1},
                {"address": 108, "name": "Import Reactive Energy (kVArh)", "f": 1},
                {"address": 110, "name": "Export Active Energy (kVArh)", "f": 1},
                {"address": 112, "name": "Aparent Energy (kVA h)", "f": 1},
                {"address": 114, "name": "Active Power (kW)", "f": 0.1},
                {"address": 116, "name": "Reactive Power (kVAr)", "f": 0.1},
                {"address": 118, "name": "Aparent Power (kVA)", "f": 0.1},
                {"address": 120, "name": "Voltage L-N (V)", "f": 1},
                {"address": 122, "name": "Current (A)", "f": 0.01},
                {"address": 124, "name": "Power Factor", "f": 0.1},
                {"address": 126, "name": "Frequency (Hz)", "f": 1},
                {"address": 128, "name": "Maximum Demand Active Power (kW)", "f": 0.1},
                {"address": 130, "name": "Maximum Demand Reactive Power (kVAr)", "f": 0.1},
                {"address": 132, "name": "Maximum Demand Apparent Power (kVA)", "f": 1},
            ]
            minimalmodbus.BAUDRATE = 9600
            instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
            instrument.serial.baudrate = 9600
            instrument.serial.timeout = 1
            for x in modbusAddress:
                val = instrument.read_register(x.get("address"), 2, 4) * x.get("f")
                x["value"] = val
                time.sleep(0.05)
            return next((x for x in modbusAddress if x["address"] == 114), 0)
        except:
            return {"address": 114, "name": "Active Power (kW)", "f": 0.1, "value": 0}

    def getBatteryVoltage(self):
        vals = []
        for i in range(10):
            self.bus.write_byte(self.adc_address, self.battery_input)
            value = self.bus.read_byte(self.adc_address)
            value = value * 125 / 140
            voltage = (value / 51) * 5.25
            vals.append(voltage)
            time.sleep(0.1)
        return sum(vals) / len(vals)

    def readEM2M2Values(self):
        try:
            Uges = self.ina.voltage() + self.ina.shunt_voltage() / 1000
            voltage = round(self.ina.voltage(), 3)
            current = self.ina.current()
            power = round(self.ina.power(), 3)
            supply = round(self.ina.supply_voltage(), 3)
            shuntV = round(self.ina.shunt_voltage(), 3)
            return power
        except:
            return 0

    def readEM2M1Values(self):
        try:
            Uges = self.ina2.voltage() + self.ina2.shunt_voltage() / 1000
            voltage = round(self.ina2.voltage(), 3)
            current = self.ina2.current()
            power = round(self.ina2.power(), 3)
            supply = round(self.ina2.supply_voltage(), 3)
            shuntV = round(self.ina2.shunt_voltage(), 3)
            print(str(voltage) + "V " + str(current) + "mA " + str(power) + "mW | supply: " + str(supply) + "V | shunt: " + str(shuntV) + "mV | Uges: " + str(Uges) + "V")
            return power
        except:
            return 0
