from pydantic import BaseModel, ConfigDict


class PersonDTO(BaseModel):
    name: str
    age: int | None = None
    address: str | None = None
    work: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ValidationErrorResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "message": "Invalid request",
            "errors": [
                {
                    "type": "type of error",
                    "msg": "error message",
                    "loc": "error location"
                }
            ]
        }
    )


class ErrorResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "not found"
            }
        }
    )
