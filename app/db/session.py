from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import SQLAlchemy


engine = create_engine(SQLAlchemy.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
