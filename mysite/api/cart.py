from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import Cart
from mysite.db.schema import CartSchema
from typing import List


cart_router = APIRouter(prefix='/cart', tags=['cart'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@cart_router.post('/create', response_model=CartSchema)
async def create_cart(cart_data: CartSchema, db: Session = Depends(get_db)):
    cart_db = Cart(**cart_data.dict())
    db.add(cart_db)
    db.commit()
    db.refresh(cart_db)
    return cart_db

@cart_router.get('/list', response_model=List[CartSchema])
async def list_cart(db: Session= Depends(get_db)):
    cart_db = db.query(Cart).all()
    return cart_db

@cart_router.get('/detail', response_model=CartSchema)
async def detail_cart(cart_id: int, db: Session = Depends(get_db)):
    cart_db = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday cart jok')
    return cart_db

@cart_router.put('/update')
async def update_review(cart_id: int, cart_data: CartSchema, db: Session = Depends(get_db)):
    cart_db = db.query(Cart).filter(Cart.id == cart_id).first()
    if not  cart_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday cart jok')
    for cart_key, cart_value in cart_data.dict().items():
        setattr(cart_db, cart_key, cart_value)
    db.commit()
    db.refresh(cart_db)
    return cart_db

@cart_router.delete('/delete')
async def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart_db = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday cart jok')
    db.delete(cart_db)
    db.commit()
    return {'message': 'success deleted'}