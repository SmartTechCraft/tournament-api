from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

config = dotenv_values('.env')

engine = create_engine("mysql+pymysql://root:1234@localhost:3306/liga_backend") #NOTE: add env variable here
connection = engine.connect()

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
