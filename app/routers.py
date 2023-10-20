from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
#from database import get_db
from database.database import app_db

import services as PersonService
from schemas import PersonDTO
from responses import ResponsesEnum

router = APIRouter(prefix='', tags=['Person REST API operations'])


@router.get('/', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.GettingAllPersonsResponse.value
            })
async def get_all_persons(db: Session = Depends(app_db.get_db)):
    persons = PersonService.get_all_persons(db)
    results = []
    for person in persons:
        results.append(ResponsesEnum.get_person_model_response(person))
    return results


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_class=Response,
             responses={
                 status.HTTP_201_CREATED: ResponsesEnum.CreatedNewPersonResponce.value,
                 status.HTTP_400_BAD_REQUEST: ResponsesEnum.InvalidDataResponse.value,
             })
async def create_person(data: PersonDTO = None, db: Session = Depends(app_db.get_db)):
    person = PersonService.create_person(data, db)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"/api/v1/persons/{person.id}"}
    )


@router.get('/{id}', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.PersonByIDResponse.value,
                status.HTTP_404_NOT_FOUND: ResponsesEnum.NotFoundPersonByIdResponse.value,
            })
async def get_person(id: int = None, db: Session = Depends(app_db.get_db)):
    person = PersonService.get_person(id, db)
    return ResponsesEnum.get_person_model_response(person)


@router.patch('/{id}', status_code=status.HTTP_200_OK,
              responses={
                  status.HTTP_200_OK: ResponsesEnum.PersonByIDUpdateResponse.value,
                  status.HTTP_400_BAD_REQUEST: ResponsesEnum.InvalidDataResponse.value,
                  status.HTTP_404_NOT_FOUND: ResponsesEnum.NotFoundPersonByIdResponse.value
              })
async def update_person(data: PersonDTO = None, id: int = None, db: Session = Depends(app_db.get_db)):
    person = PersonService.update_person(data, id, db)
    return ResponsesEnum.get_person_model_response(person)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT,
               response_class=Response,
               responses={
                   status.HTTP_204_NO_CONTENT: ResponsesEnum.PersonByIDDeleteResponse.value
               })
async def delete_person(id: int = None, db: Session = Depends(app_db.get_db)):
    PersonService.delete_person(id, db)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
