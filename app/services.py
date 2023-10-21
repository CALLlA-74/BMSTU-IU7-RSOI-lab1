from models import Person
from sqlalchemy.orm import Session
from schemas import PersonDTO
from fastapi import status
from fastapi.exceptions import HTTPException


def create_person(data: PersonDTO, db: Session):
    person = Person(name=data.name, age=data.age, address=data.address, work=data.work)

    try:
        db.add(person)
        db.commit()
        db.refresh(person)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if person is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return person


def get_all_persons(db: Session):
    return db.query(Person).all()


def get_person(id: int, db: Session):
    person = db.query(Person).filter(Person.id == id).first()
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return person


def update_person(data: PersonDTO, id: int, db: Session):
    person = db.query(Person).filter(Person.id == id).first()
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if data.name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    person.name = data.name
    if data.age:
        person.age = data.age
    if data.address:
        person.address = data.address
    if data.work:
        person.work = data.work

    db.add(person)
    db.commit()
    db.refresh(person)

    return person


def delete_person(id: int, db: Session):
    num_of_removed_rows = db.query(Person).filter(Person.id == id).delete()
    db.commit()

    return num_of_removed_rows
