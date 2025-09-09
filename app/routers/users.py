from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserLogin, UserUpdate
from app.services.user_service import UserService
from app.utils.pagination import paginate
from app.utils.db_utils import get_or_404

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, user_data)

@router.get("/", response_model=List[UserOut])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return paginate(db.query(User), skip, limit)

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.get_user(db, user_id)

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    return UserService.update_user(db, user_id, user_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    UserService.delete_user(db, user_id)
    return
