# app/services/user_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(status_code=400, detail="Username déjà utilisé")
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(status_code=400, detail="Email déjà utilisé")
        
        hashed_password = pwd_context.hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=getattr(User, "hashed_password").impl.python_type(hashed_password),
            role=user_data.role.lower() if user_data.role else "user"
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def login_user(db: Session, login_data: UserLogin) -> User:
        db_user = db.query(User).filter(User.username == login_data.username).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="Utilisateur introuvable")

        hashed_password = getattr(db_user, "hashed_password")  # ✅ Comme dans le router
        if not pwd_context.verify(login_data.password, hashed_password):
            raise HTTPException(status_code=400, detail="Mot de passe incorrect")
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        # Mise à jour du mot de passe avec contournement type
        if user_data.password:
            hashed = pwd_context.hash(user_data.password)
            setattr(user, "hashed_password", hashed)

        for field, value in user_data.dict(exclude_unset=True, exclude={"password"}).items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        return user

    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        db.delete(user)
        db.commit()
