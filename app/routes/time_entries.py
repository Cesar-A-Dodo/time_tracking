from fastapi import APIRouter

router = APIRouter(
    prefix="/time_entries",
    tags=["Time Entry"]
)
