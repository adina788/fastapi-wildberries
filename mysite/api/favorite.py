from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import Favorite
from mysite.db.schema import FavoriteSchema
from typing import List


favorite_router = APIRouter(prefix='/favorite', tags=['favorite'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@favorite_router.post('/create', response_model=FavoriteSchema)
async def create_favorite(favorite_data: FavoriteSchema, db: Session = Depends(get_db)):
    favorite_db = Favorite(**favorite_data.dict())
    db.add(favorite_db)
    db.commit()
    db.refresh(favorite_db)
    return favorite_db

@favorite_router.get('/list', response_model=List[FavoriteSchema])
async def list_favorite(db: Session= Depends(get_db)):
    favorite_db = db.query(Favorite).all()
    return favorite_db

@favorite_router.get('/detail', response_model=FavoriteSchema)
async def detail_favorite(favorite_id: int, db: Session = Depends(get_db)):
    favorite_db = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if not favorite_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday favorite jok')
    return favorite_db

@favorite_router.put('/update')
async def update_favorite(favorite_id: int, favorite_data: FavoriteSchema, db: Session = Depends(get_db)):
    favorite_db = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if not favorite_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday favorite jok')
    for favorite_key, favorite_value in favorite_data.dict().items():
        setattr(favorite_db, favorite_key, favorite_value)
    db.commit()
    db.refresh(favorite_db)
    return favorite_db

@favorite_router.delete('/delete')
async def delete_favorite(favorite_id: int, db: Session = Depends(get_db)):
    favorite_db = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if not favorite_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday favorite jok')
    db.delete(favorite_db)
    db.commit()
    return {'message': 'success deleted'}