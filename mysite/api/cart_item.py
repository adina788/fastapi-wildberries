from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import CartItem
from mysite.db.schema import CartItemSchema
from typing import List


cart_item_router = APIRouter(prefix='/cart_item', tags=['cart_item'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@cart_item_router.post('/create', response_model=CartItemSchema)
async def create_cart_item(cart_item_data: CartItemSchema, db: Session = Depends(get_db)):
    cart_item_db = CartItem(**cart_item_data.dict())
    db.add(cart_item_db)
    db.commit()
    db.refresh(cart_item_db)
    return cart_item_db

@cart_item_router.get('/list', response_model=List[CartItemSchema])
async def list_cart_item(db: Session= Depends(get_db)):
    cart_item_db = db.query(CartItem).all()
    return cart_item_db

@cart_item_router.get('/detail', response_model=CartItemSchema)
async def detail_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
    cart_item_db = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday cart_item jok')
    return cart_item_db

@cart_item_router.put('/update')
async def update_cart_item(cart_item_id: int,cart_item_data: CartItemSchema, db: Session = Depends(get_db)):
    cart_item_db = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday cart_item jok')
    for cart_item_key, cart_item_value in cart_item_data.dict().items():
        setattr(cart_item_db, cart_item_key, cart_item_value)
    db.commit()
    db.refresh(cart_item_db)
    return cart_item_db

@cart_item_router.delete('/delete')
async def delete_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
    cart_item_db = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday cart_item jok')
    db.delete(cart_item_db)
    db.commit()
    return {'message': 'success deleted'}