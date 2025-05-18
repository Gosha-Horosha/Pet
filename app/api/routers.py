from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from app.db.session import current_session
from app.models import Boys, Girls, PairReview, Conscription
from app.schema import *

router = APIRouter()


# --- Boys Routes ---
@router.post("/boys/", response_model=Boy, status_code=status.HTTP_201_CREATED)
def create_boy(boy: BoyCreate, db: Session = Depends(current_session)):
    db_boy = Boys(**boy.model_dump())
    db.add(db_boy)
    db.commit()
    # db.refresh(db_boy)
    return db_boy


@router.get("/boys/", response_model=List[Boy])
def read_boys(skip: int = 0, limit: int = 100, db: Session = Depends(current_session)):
    boys = db.scalars(select(Boys).offset(skip).limit(limit)).all()
    return boys


@router.get("/boys/{boy_id}", response_model=Boy)
def read_boy(boy_id: int, db: Session = Depends(current_session)):
    boy = db.get(Boys, boy_id)
    if not boy:
        raise HTTPException(status_code=404, detail="Boy not found")
    return boy


@router.put("/boys/{boy_id}", response_model=Boy)
def update_boy(boy_id: int, boy: BoyUpdate, db: Session = Depends(current_session)):
    db_boy = db.get(Boys, boy_id)
    if not db_boy:
        raise HTTPException(status_code=404, detail="Boy not found")

    update_data = boy.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_boy, field, value)

    db.commit()
    db.refresh(db_boy)
    return db_boy


@router.delete("/boys/{boy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_boy(boy_id: int, db: Session = Depends(current_session)):
    boy = db.get(Boys, boy_id)
    if not boy:
        raise HTTPException(status_code=404, detail="Boy not found")

    db.delete(boy)
    db.commit()
    return None


# --- Girls Routes ---
@router.post("/girls/", response_model=Girl, status_code=status.HTTP_201_CREATED)
def create_girl(girl: GirlCreate, db: Session = Depends(current_session)):
    db_girl = Girls(**girl.model_dump())
    db.add(db_girl)
    db.commit()
    db.refresh(db_girl)
    return db_girl


@router.get("/girls/", response_model=List[Girl])
def read_girls(skip: int = 0, limit: int = 100, db: Session = Depends(current_session)):
    girls = db.scalars(select(Girls).offset(skip).limit(limit)).all()
    return girls


@router.get("/girls/{girl_id}", response_model=Girl)
def read_girl(girl_id: int, db: Session = Depends(current_session)):
    girl = db.get(Girls, girl_id)
    if not girl:
        raise HTTPException(status_code=404, detail="Girl not found")
    return girl


# --- Pair Reviews Routes ---
@router.post("/reviews/", response_model=Review, status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewCreate, db: Session = Depends(current_session)):
    # Проверка существования связи между мальчиком и девочкой
    boy = db.get(Boys, review.boy_id)
    girl = db.get(Girls, review.girl_id)

    if not boy or not girl:
        raise HTTPException(
            status_code=400,
            detail="Boy or girl not found"
        )

    db_review = PairReview(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/reviews/{review_id}", response_model=Review)
def read_review(review_id: int, db: Session = Depends(current_session)):
    review = db.get(PairReview, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


# --- Conscription Routes ---
@router.post("/conscription/", response_model=Conscription, status_code=status.HTTP_201_CREATED)
def create_conscription(conscription: ConscriptionCreate, db: Session = Depends(current_session)):
    boy = db.get(Boys, conscription.boy_id)
    if not boy:
        raise HTTPException(status_code=404, detail="Boy not found")

    db_conscription = Conscription(**conscription.model_dump())
    db.add(db_conscription)
    db.commit()
    db.refresh(db_conscription)
    return db_conscription


@router.get("/boys/{boy_id}/conscription", response_model=Conscription)
def read_boy_conscription(boy_id: int, db: Session = Depends(current_session)):
    conscription = db.scalar(
        select(Conscription).where(Conscription.boy_id == boy_id)
    )
    if not conscription:
        raise HTTPException(
            status_code=404,
            detail="Conscription record not found for this boy"
        )
    return conscription