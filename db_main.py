import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:nanogrid@127.0.0.1:3306/fyp_prjct")
Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()
