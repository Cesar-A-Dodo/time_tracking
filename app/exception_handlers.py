from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.services.exceptions import (
    ServiceError,

    EmployeeInactiveError,
    OpenTimeEntryExistsError,
    InvalidStatusTransitionError,
    TimeEntryAlreadyFinalizedError,
    ActivityInactiveError,
    ActivityNotFoundError,

    EmployeeNotFoundError,
    EmployeeAlreadyInactiveError,

    ActivityAlreadyInactiveError,
)


def _error(status_code: int, error_code: str, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "detail": detail},
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(EmployeeNotFoundError)
    async def employee_not_found_handler(request: Request, exc: EmployeeNotFoundError):
        return _error(404, "EMPLOYEE_NOT_FOUND", str(exc))

    @app.exception_handler(ActivityNotFoundError)
    async def activity_not_found_handler(request: Request, exc: ActivityNotFoundError):
        return _error(404, "ACTIVITY_NOT_FOUND", str(exc))

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return _error(404, "NOT_FOUND", str(exc))

    @app.exception_handler(EmployeeAlreadyInactiveError)
    async def employee_already_inactive_handler(request: Request, exc: EmployeeAlreadyInactiveError):
        return _error(409, "EMPLOYEE_ALREADY_INACTIVE", str(exc))

    @app.exception_handler(ActivityAlreadyInactiveError)
    async def activity_already_inactive_handler(request: Request, exc: ActivityAlreadyInactiveError):
        return _error(409, "ACTIVITY_ALREADY_INACTIVE", str(exc))

    @app.exception_handler(OpenTimeEntryExistsError)
    async def open_time_entry_exists_handler(request: Request, exc: OpenTimeEntryExistsError):
        return _error(409, "OPEN_TIME_ENTRY_EXISTS", str(exc))

    @app.exception_handler(TimeEntryAlreadyFinalizedError)
    async def time_entry_already_finalized_handler(request: Request, exc: TimeEntryAlreadyFinalizedError):
        return _error(409, "TIME_ENTRY_ALREADY_FINALIZED", str(exc))

    @app.exception_handler(EmployeeInactiveError)
    async def employee_inactive_handler(request: Request, exc: EmployeeInactiveError):
        return _error(400, "EMPLOYEE_INACTIVE", str(exc))

    @app.exception_handler(ActivityInactiveError)
    async def activity_inactive_handler(request: Request, exc: ActivityInactiveError):
        return _error(400, "ACTIVITY_INACTIVE", str(exc))

    @app.exception_handler(InvalidStatusTransitionError)
    async def invalid_status_transition_handler(request: Request, exc: InvalidStatusTransitionError):
        return _error(400, "INVALID_STATUS_TRANSITION", str(exc))

    @app.exception_handler(ServiceError)
    async def service_error_handler(request: Request, exc: ServiceError):
        return _error(400, "SERVICE_ERROR", str(exc))
    