from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import RefreshToken
from mysite.db.schema import RefreshTokenSchema
from typing import List


refresh_token_router = APIRouter(prefix='/refresh_token', tags=['refresh_token'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@refresh_token_router.post('/create', response_model=RefreshTokenSchema)
async def create_refresh_token(refresh_token_data: RefreshTokenSchema, db: Session = Depends(get_db)):
    refresh_token_db = RefreshToken(**refresh_token_data.dict())
    db.add(refresh_token_db)
    db.commit()
    db.refresh(refresh_token_db)
    return refresh_token_db

@refresh_token_router.get('/list', response_model=List[RefreshTokenSchema])
async def list_refresh_token(db: Session= Depends(get_db)):
    refresh_token_db = db.query(RefreshToken).all()
    return refresh_token_db

@refresh_token_router.get('/detail', response_model=RefreshTokenSchema)
async def detail_refresh_token(refresh_token_id: int, db: Session = Depends(get_db)):
    refresh_token_db = db.query(RefreshToken).filter(RefreshToken.id == refresh_token_id).first()
    if not refresh_token_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday refresh_token jok')
    return refresh_token_db

@refresh_token_router.put('/update')
async def update_refresh_token(refresh_token_id: int, refresh_token_data: RefreshTokenSchema, db: Session = Depends(get_db)):
    refresh_token_db = db.query(RefreshToken).filter(RefreshToken.id == refresh_token_id).first()
    if not refresh_token_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday refresh_token jok')
    for refresh_token_key, refresh_token_value in refresh_token_data.dict().items():
        setattr(refresh_token_db, refresh_token_key, refresh_token_value)
    db.commit()
    db.refresh(refresh_token_db)
    return refresh_token_db

@refresh_token_router.delete('/delete')
async def delete_refresh_token(refresh_token_id: int, db: Session = Depends(get_db)):
    refresh_token_db = db.query(RefreshToken).filter(RefreshToken.id == refresh_token_id).first()
    if not refresh_token_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday refresh_token jok')
    db.delete(refresh_token_db)
    db.commit()
    return {'message': 'success deleted'}