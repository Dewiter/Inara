from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/", response_model=list[UserResponse], name="read root")
def get_commodities():
