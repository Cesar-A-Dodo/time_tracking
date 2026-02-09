from fastapi import APIRouter

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

@router.get("/")
def list_employees():
    return {"message": "Lista de funcionários"}