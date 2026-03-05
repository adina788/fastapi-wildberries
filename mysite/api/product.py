from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import Product
from mysite.db.schema import ProductSchema
from typing import List


product_router = APIRouter(prefix='/product', tags=['Product'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_router.post('/create', response_model=ProductSchema)
async def create_product(product_data: ProductSchema, db: Session = Depends(get_db)):
    product_db = Product(**product_data.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db

@product_router.get('/list', response_model=List[ProductSchema])
async def list_product(db: Session = Depends(get_db)):
    product_db = db.query(Product).all()
    return product_db

@product_router.get('/detail', response_model=ProductSchema)
async def detail_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday product jok')
    return product_db

@product_router.put('/update')
async def update_product(product_id: int, product_data: ProductSchema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday product jok')
    for product_key, product_value in product_data.dict().items():
        setattr(product_db, product_key, product_value)
    db.commit()
    db.refresh(product_db)
    return product_db

@product_router.delete('/delete')
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday product jok')
    db.delete(product_db)
    db.commit()
    return {'message': 'success deleted'}