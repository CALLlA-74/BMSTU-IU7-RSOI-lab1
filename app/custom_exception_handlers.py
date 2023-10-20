from main import app
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.encoders import jsonable_encoder


@app.exception_handler(RequestValidationError)
async def custom_request_validation_error_handle(exc: RequestValidationError):
    errors = jsonable_encoder(exc.errors())
    error_details = []

    for error in errors:
        details = {}
        details["type"] = error["type"]
        details["message"] = error['msg']

        error_details.append(details)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": "Invalid request",
            "errors": error_details
        }
    )


@app.exception_handler(HTTPException)
async def custom_http_exception_handle(exc: HTTPException):
    return JSONResponse(status_code=exc.status_code,
                        content={"message": exc.detail})
