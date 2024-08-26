from db.db_main import Base
import sqlalchemy

class HistoryData(Base):
    __tablename__ = "history_data"
    
    id = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True, autoincrement=True, nullable=False)
    day = sqlalchemy.Column(sqlalchemy.String(10))
    time_slot = sqlalchemy.Column(sqlalchemy.INT)
    created_date = sqlalchemy.Column(sqlalchemy.DATETIME)
    dc_watt = sqlalchemy.Column(sqlalchemy.FLOAT)
    ac_watt = sqlalchemy.Column(sqlalchemy.FLOAT)
    date = sqlalchemy.Column(sqlalchemy.DATE)
