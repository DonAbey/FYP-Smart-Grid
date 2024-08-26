import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Orders(Base):
    __tablename__ = "Orders"
    id = sqlalchemy.Column(sqlalchemy.String(10), primary_key=True)
    col = sqlalchemy.Column(sqlalchemy.String(10))

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:12345678@127.0.0.1:3306/test")
Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

orders = Orders(id="1", col="test")
session.add(orders)
session.commit()
