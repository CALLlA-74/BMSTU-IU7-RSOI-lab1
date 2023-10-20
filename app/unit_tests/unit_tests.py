from copy import deepcopy

from unit_tests.mock_data import PersonsMock
from database import Database
from schemas import PersonDTO
from fastapi.exceptions import HTTPException
from fastapi import status
import services as PersonService

persons = deepcopy(PersonsMock.mocks)
correct_persons = {}
test_db = Database("sqlite:///../test_db/persons.db")
test_db.create_all()


def check_equality(a: dict, b: dict):
    return (a['name'] == b['name'] and
            a['age'] == b['age'] and
            a['address'] == b['address'] and
            a['work'] == b['work'])


def init_db(database: Database, init_data: list):
    db = database.get_db()
    for data in init_data:
        person_dto = PersonDTO(
            name=data['name'],
            age=data['age'],
            address=data['address'],
            work=data['work']
        )
        person = PersonService.create_person(person_dto, db).get_json_model()
        assert check_equality(person, data), 'Initial error: ' + person + " != " + data
        data['id'] = person['id']


def init_correct_persons(data: list, correct_data: dict):
    for person in data:
        correct_data[person['id']] = person


init_db(test_db, persons)
init_correct_persons(persons, correct_persons)


async def test_get_all_persons_success():
    try:
        all_persons = PersonService.get_all_persons(test_db.get_db())
        assert len(all_persons) == len(correct_persons), 'Error getting all persons: ' + str(
            len(all_persons)) + ' != ' + str(len(correct_persons))
        for idx in range(len(all_persons)):
            person = all_persons[idx].get_json_model()
            assert check_equality(person, correct_persons[
                person['id']]), 'Error getting all persons: equality error ' + person + ' ' + correct_persons[
                person['id']]
    except Exception as e:
        assert False, 'Exception getting all persons: ' + str(e)


async def test_get_by_id_success():
    try:
        for person in persons:
            recieved_person = PersonService.get_person(person['id'], test_db.get_db()).get_json_model()
            assert (check_equality(recieved_person, person),
                    'Error in getting person by id (success): equality error ' + recieved_person + ' ' + correct_persons[person['id']])
    except Exception as e:
        assert False, 'Exception in getting all person by id (success): ' + str(e)


async def test_get_by_id_not_found():
    try:
        PersonService.get_person(max(correct_persons.keys()) + 1, test_db.get_db())
        assert False, 'Error in getting all person by id (not_found): no 404 exception'
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            assert True
        assert False, 'HTTPException in getting all person by id (not_found): HTTPException is not 404: ' + e.detail
    except Exception as e:
        assert False, 'Exception in getting all person by id (not_found): ' + str(e)


async def test_delete_by_id_success():
    try:
        ids = correct_persons.keys()
        person = PersonService.delete_person(ids[0], test_db.get_db()).get_json_model()
        assert (check_equality(person, correct_persons[ids[0]]),
                'Error in deleting person: equality error: ' + person + ' != ' + correct_persons[ids[0]])
    except Exception as e:
        assert False, 'Exception in deleting person: ' + str(e)


async def test_update_by_id_success():
    try:
        ids = correct_persons.keys()
        update_data = PersonDTO(
            name="Martin",
            age=22,
            address="New York",
            work=None
        )
        person = PersonService.update_person(update_data, ids[0], test_db.get_db()).get_json_model()
        assert not check_equality(person, correct_persons[ids[0]]), 'Error in updating person (success): ' + person + ' is equal ' + correct_persons[ids[0]]
    except Exception as e:
        assert False, 'Exception in updating person: ' + str(e)


async def test_update_by_id_not_found():
    try:
        update_data = PersonDTO(
            name="Martin",
            age=22,
            address="New York",
            work=None
        )
        id = max(correct_persons.keys()) + 1
        PersonService.update_person(update_data, id, test_db.get_db()).get_json_model()
        assert False, 'in updating person (not found): no 404 exception'
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            assert True
        assert False, 'HttpException in updating person: is not 404 exception ' + str(e)
    except Exception as e:
        assert False, 'Exception in updating person: is not 404 exception ' + str(e)
