from sqlalchemy import Integer, String, Column
from database.database import app_db     # Base


class Person(app_db.Base):
    __tablename__ = 'persons'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    address = Column(String)
    work = Column(String)

    def get_json_model(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "address": self.address,
            "work": self.work
        }
