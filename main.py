from services.device_measurements import DeviceMeasurements
from services.data_service import DataService
import time
from RPLCD.i2c import CharLCD

deviceMeasurements = DeviceMeasurements()
dataService = DataService()
initial = True
last_checked_time_slot = 0
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, cols=20, rows=4)
charging = False

def getCurrentTotalWatt():
    EM2M2 = deviceMeasurements.readEM2M2Values() / 1000
    return EM2M2

def getCurrentDCWatt():
    return deviceMeasurements.readEM2M2Values() / 1000

def getCurrentACWatt():
    return (deviceMeasurements.readEM2M3Values())["value"]

def currentBatteryTotalWatt():
    batV = deviceMeasurements.getBatteryVoltage()
    return batV * 2 * 7

def currentBatteryPercentage():
    batV = deviceMeasurements.getBatteryVoltage()
    print("Battery Voltage : " + str(batV))
    percent = ((batV - 11) * 100 / (13 - 11))
    return percent if percent < 100 else 100

ac_wattH_total = 0
dc_wattH_total = 0

while 1:
    curr = dataService.getCurrentTimeSlot()
    batW = currentBatteryTotalWatt()
    batPercent = currentBatteryPercentage()
    currW = getCurrentTotalWatt()
    
    if batPercent > 20:
        print("Battery Percentage > 20% " + str(batPercent) + "%")
        if initial or (curr["curr_time_slot"] != last_checked_time_slot):
            last_checked_time_slot = curr["curr_time_slot"]
            if not initial:
                print("Adding Data")
                dataService.addNewData(dc_wattH_total, ac_wattH_total)
                dc_wattH_total = 0
                ac_wattH_total = 0
            needed_watt = dataService.getNeededTotalWatt()
            print(str(needed_watt) + "\t" + str(batW))
            if needed_watt < batW:
                deviceMeasurements.batteryDischargingMode()
                charging = False
            else:
                deviceMeasurements.batteryChargingMode(curr["curr_time_slot"])
                charging = True

        if batW * 0.9 < currW:
            deviceMeasurements.batteryChargingMode(curr["curr_time_slot"])
            charging = True
            print("Emergency Scenario. Battery Charging mode for next 2 hours.")
    else:
        print("Battery Percentage low. Battery Charging mode" + str(batPercent))
        deviceMeasurements.batteryChargingMode(curr["curr_time_slot"])
        charging = True
    
    initial = False
    
    ac_wattH_total += getCurrentACWatt() * ((1 * (5 / 60)) / 60)
    dc_wattH_total += getCurrentDCWatt() * ((1 * (5 / 60)) / 60)
    
    try:
        lcd.clear()
        lcd.write_string("Battery :- " + str(round(batPercent)) + " %\r\n" + ("Battery charging" if charging else "Battery Discharging"))
    except:
        try:
            lcd = CharLCD(i2c_expander='PCF8574', address=0x27, cols=20, rows=4)
        except:
            print("LCD ERROR")
    
    time.sleep(1 * 5)
