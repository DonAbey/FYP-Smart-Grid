from services.db_service import DBService
from datetime import datetime
import pytz

class DataService:
    time_arr = [
        {"up": 0, "down": 2},
        {"up": 2, "down": 4},
        {"up": 4, "down": 6},
        {"up": 6, "down": 8},
        {"up": 8, "down": 10},
        {"up": 10, "down": 12},
        {"up": 12, "down": 14},
        {"up": 14, "down": 16},
        {"up": 16, "down": 18},
        {"up": 18, "down": 20},
        {"up": 20, "down": 22},
        {"up": 22, "down": 24},
    ]

    def getNeededTotalWatt(self):
        curr = self.getCurrentTimeSlot()
        data = DBService.getLastFourWeekData(curr["curr_day"], curr["curr_time_slot"])
        dc_watt_avg = sum(d.dc_watt for d in data) / data.count()
        ac_watt_avg = sum(d.ac_watt for d in data) / data.count()
        total_watt_avg = dc_watt_avg + ac_watt_avg
        return total_watt_avg

    def addNewData(self, dc_watt, ac_watt):
        curr = self.getCurrentTimeSlot()
        data = DBService.addRecord(curr["curr_day"], curr["curr_time_slot"], dc_watt, ac_watt)

    def getCurrentTimeSlot(self):
        curr_date = datetime.now(pytz.timezone('Asia/Colombo'))
        curr_day = curr_date.strftime('%A')
        curr_hour = curr_date.hour
        curr_time_slot = [
            idx for idx, time_slot in enumerate(self.time_arr)
            if time_slot['up'] <= curr_hour and time_slot['down'] > curr_hour
        ]
        return {"curr_day": curr_day, "curr_time_slot": curr_time_slot[0]}
