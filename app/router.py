from fastapi import APIRouter
from app.routes import employees, activities
from time_tracking.app.routes import time_entries

api_router = APIRouter()

api_router.include_router(employees.router)
api_router.include_router(activities.router)
api_router.include_router(time_entries.router)