from db.db_main import session
from models.history_data import HistoryData
import sqlalchemy
from datetime import datetime
import pytz

class DBService:
    def getLastFourWeekData(day, time_slot):
        data = session.query(HistoryData).filter(
            (HistoryData.day == day) & (HistoryData.time_slot == time_slot)
        ).order_by(sqlalchemy.desc(HistoryData.date)).limit(4)
        return data

    def addRecord(day, time_slot, dc_watt, ac_watt):
        currDateTime = datetime.now(pytz.timezone('Asia/Colombo'))
        historyData = HistoryData(
            day = day,
            time_slot = time_slot,
            created_date = currDateTime,
            dc_watt = dc_watt,
            ac_watt = ac_watt,
            date = currDateTime.strftime("%Y-%m-%d")
        )
        session.add(historyData)
        session.commit()
