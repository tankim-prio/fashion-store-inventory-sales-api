from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth_dependency import get_current_user
from app.models.user import User
from app.schemas.user import TokenResponse, UserProfileUpdate, UserRegister, UserResponse
from app.services.auth_service import (
    deactivate_current_profile,
    login_user,
    register_user,
    update_current_profile,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    return register_user(db=db, user_data=user)


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(db=db, email=form_data.username, password=form_data.password)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/profile", response_model=TokenResponse)
def update_my_profile(
    profile: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_current_profile(
        db=db,
        current_user=current_user,
        profile_data=profile
    )


@router.delete("/profile")
def delete_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return deactivate_current_profile(db=db, current_user=current_user)
