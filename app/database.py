from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import get_db_url

Base = declarative_base()


class Database:
    def __init__(self, db_url=get_db_url()):
        self.DB_URL = db_url
        print("URL: " + db_url)
        print(db_url[:6] + "; " + str(db_url[:6] != "sqlite"))

        if db_url[:6] != "sqlite":
            self.engine = create_engine(self.DB_URL)
        else:
            self.engine = create_engine(self.DB_URL, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_all(self):
        Base.metadata.create_all(bind=self.engine)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close_all()


#app_db = Database()

"""DB_URL = get_db_url()   # "sqlite:///../postgres/persons.db"

engine = create_engine(DB_URL)  # connect_args={"check_same_thread": False}
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()
"""
