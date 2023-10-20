from enum import Enum
from schemas import PersonDTO, ValidationErrorResponse, ErrorResponse
from models import Person as PersonModel


class ResponsesEnum(Enum):
    GettingAllPersonsResponse = {
        "model": list[PersonDTO],
        "description": "All Persons",
    }

    CreatedNewPersonResponce = {
        "description": "Created new Person",
        "headers": {
            "Location": {
                "description": "Path to new Person",
                "style": "simple",
                "schema": {
                    "type": "string"
                }
            },
        },

    }

    InvalidDataResponse = {
        "description": "Invalid data",
        "model": ValidationErrorResponse,
    }

    PersonByIDResponse = {
        "description": "Person by ID",
        "model": PersonDTO,
    }

    NotFoundPersonByIdResponse = {
        "description": "Not found Person by ID",
        "model": ErrorResponse,
    }

    PersonByIDUpdateResponse = {
        "description": "Person by ID was updated",
        "model": PersonDTO,
    }

    PersonByIDDeleteResponse = {
        "description": "Person for ID was removed",
    }

    @staticmethod
    def get_person_model_response(person: PersonModel):
        return person.get_json_model()
