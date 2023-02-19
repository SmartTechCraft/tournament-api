from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from decouple import config

CONNECTION_STRING = config("DB_CONNECT_STRING")

engine = create_engine(CONNECTION_STRING) 
connection = engine.connect()

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
