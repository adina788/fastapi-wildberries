from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import Review
from mysite.db.schema import ReviewSchema
from typing import List


review_router = APIRouter(prefix='/review', tags=['Review'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@review_router.post('/create', response_model=ReviewSchema)
async def create_review(review_data: ReviewSchema, db: Session = Depends(get_db)):
    review_db = Review(**review_data.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.get('/list', response_model=List[ReviewSchema])
async def list_review(db: Session= Depends(get_db)):
    review_db = db.query(Review).all()
    return review_db

@review_router.get('/detail', response_model=ReviewSchema)
async def detail_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday maalymat jok')
    return review_db

@review_router.put('/update')
async def update_review(review_id: int, review_data: ReviewSchema, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday maalymat jok')
    for review_key, review_value in review_data.dict().items():
        setattr(review_db, review_key, review_value)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.delete('/delete')
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday maalymat jok')
    db.delete(review_db)
    db.commit()
    return {'message': 'success deleted'}