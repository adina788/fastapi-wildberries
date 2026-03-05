from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import ImageProduct
from mysite.db.schema import ImageProductSchema
from typing import List

image_product_router = APIRouter(prefix='/image_product', tags=['image_product'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@image_product_router.post('/create', response_model=ImageProductSchema)
async def create_image_product(image_product_data: ImageProductSchema, db: Session = Depends(get_db)):
    image_product_db = ImageProduct(**image_product_data.dict())
    db.add(image_product_db)
    db.commit()
    db.refresh(image_product_db)
    return image_product_db

@image_product_router.get('/list', response_model=List[ImageProductSchema])
async def get_image_product(db: Session = Depends(get_db)):
    image_product_db = db.query(ImageProduct).all()
    return image_product_db

@image_product_router.get('/detail', response_model=ImageProductSchema)
async def detail_image_product(image_product_id: int, db: Session = Depends(get_db)):
    image_product_db = db.query(ImageProduct).filter(ImageProduct.id == image_product_id).first()
    if not image_product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday image_product jok')
    return image_product_db

@image_product_router.put('/update')
async def update_image_product(image_product_id: int, image_product_data: ImageProductSchema, db: Session = Depends(get_db)):
    image_product_db = db.query(ImageProduct).filter(ImageProduct.id == image_product_id).first()
    if not image_product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday image_product jok')
    for image_product_key, image_product_value in image_product_data.dict().items():
        setattr(image_product_db, image_product_key, image_product_value)
    db.commit()
    db.refresh(image_product_db)
    return image_product_db

@image_product_router.delete('/delete')
async def delete_image_product(image_product_id: int, db: Session = Depends(get_db)):
    image_product_db = db.query(ImageProduct).filter(ImageProduct.id == image_product_id).first()
    if not image_product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday image product jok')
    db.delete(image_product_db)
    db.commit()
    return {'message': 'success deleted'}




