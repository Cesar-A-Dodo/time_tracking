from fastapi import APIRouter
from app.routes import employees, activities, time_entries, metrics

api_router = APIRouter()

api_router.include_router(employees.router)
api_router.include_router(activities.router)
api_router.include_router(time_entries.router)
api_router.include_router(metrics.router)
