from fastapi import APIRouter
from app.routes import employees, activities, time_tracking

api_router = APIRouter()

api_router.include_router(employees.router)
api_router.include_router(activities.router)
api_router.include_router(time_tracking.router)