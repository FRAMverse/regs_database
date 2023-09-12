from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import config

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# don't upload this to github again jackass.
SQLALCHEMY_DATABASE_URL = config.URI['development']

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()