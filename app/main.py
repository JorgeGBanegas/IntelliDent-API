from fastapi import FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from mangum import Mangum
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper
from starlette import status
from starlette.responses import JSONResponse
from app.config.database import Base, engine
from app.routes.patient_routes import router as patient_router
from app.routes.image_process_routes import router as image_process_router
from app.routes.dental_image_routes import router as dental_image_router
from app.routes.image_category_routes import router as image_category_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IntelliDent API",
    description="API para la aplicación IntelliDent",
    version="1.0.0"
)


@app.exception_handler(RequestValidationError)
async def http_exception_accept_handler(request: Request, exc: RequestValidationError) -> Response:
    raw_errors = exc.raw_errors
    error_wrapper: ErrorWrapper = raw_errors[0]
    validation_error: ValidationError = error_wrapper.exc
    overwritten_errors = validation_error.errors()
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content={"detail": jsonable_encoder(overwritten_errors)},
                        )

app.include_router(patient_router)
app.include_router(image_process_router)
app.include_router(dental_image_router)
app.include_router(image_category_router)

handler = Mangum(app)


@app.get("/")
async def root():
    return {
        "message": "Bienvenido a IntelliDent API",
        "version": "1.0.0",
        "author": "Jorge Gustavo Banegas Melgar",
        "email": "jorge.g.banegas@gmail.com"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host='localhost', port=8000, reload=True)
