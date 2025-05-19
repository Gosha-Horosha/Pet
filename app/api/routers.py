from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from typing import List

# from app.db.session import current_session
from app.models import Boys, Girls, PairReview, Conscription
from app.models.base import boys_girls
from app.schema.schems import *

router = APIRouter()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost/new"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def current_session():
#     current_session = Session()
#     return current_session

db = Session()

# --- Boys Routes ---
@router.post("/boys/", response_model=Boy, status_code=status.HTTP_201_CREATED)
def create_boy(boy: BoyCreate):
    db_boy = Boys(**boy.model_dump())
    db.add(db_boy)
    db.commit()
    db.refresh(db_boy)
    return db_boy


@router.get("/boys/", response_model=List[Boy])
def read_boys(limit: int = 100):
    boys = db.scalars(select(Boys).limit(limit)).all()
    return boys


@router.get("/boys/{boy_id}", response_model=Boy)
def read_boy(boy_id: int):
    boy = db.get(Boys, boy_id)
    if not boy:
        raise HTTPException(status_code=404, detail="Boy not found")
    return boy


@router.put("/boys/{boy_id}", response_model=BoyUpdate)
def update_boy(boy_id: int, boy: BoyUpdate):
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
def delete_boy(boy_id: int):
    boy = db.get(Boys, boy_id)
    if not boy:
        raise HTTPException(status_code=404, detail="Boy not found")
    if hasattr(boy, 'girls'):
        boy.girls.clear()  # Удаляем все связи many-to-many

    db.execute(delete(PairReview).where(PairReview.boy_id == boy_id))

    # boy.girls = []
    # id = boy.boy_id
    # b_g = db.execute(select(boys_girls).where(boys_girls.c.boy_id == id))
    # for p in b_g:
    #     print(p)
    #     db.delete(p)
    # pairs = db.scalars(select(PairReview).where(PairReview.boy_id == id)).all()
    # for p in pairs:
    #     db.delete(p)
    db.delete(boy)

    db.commit()
    return None


# --- Girls Routes ---
@router.post("/girls/", response_model=Girl, status_code=status.HTTP_201_CREATED)
def create_girl(girl: GirlCreate):
    db_girl = Girls(**girl.model_dump())
    db.add(db_girl)
    db.commit()
    db.refresh(db_girl)
    return db_girl


@router.get("/girls/", response_model=List[Girl])
def read_girls(limit: int = 100):
    girls = db.scalars(select(Girls).limit(limit)).all()
    return girls


@router.get("/girls/{girl_id}", response_model=Girl)
def read_girl(girl_id: int):
    girl = db.get(Girls, girl_id)
    if not girl:
        raise HTTPException(status_code=404, detail="Girl not found")
    return girl


@router.post("/reviews/", response_model=Review, status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewCreate):
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
def read_review(review_id: int):
    review = db.get(PairReview, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


# --- Conscription Routes ---
@router.post("/conscription/", response_model=Conscription, status_code=status.HTTP_201_CREATED)
def create_conscription(conscription: ConscriptionCreate):
    boy = db.get(Boys, conscription.boy_id)
    if not boy:
        raise HTTPException(status_code=404, detail="Boy not found")

    db_conscription = Conscription(**conscription.model_dump())
    db.add(db_conscription)
    db.commit()
    db.refresh(db_conscription)
    return db_conscription


@router.get("/boys/{boy_id}/conscription", response_model=Conscription)
def read_boy_conscription(boy_id: int):
    conscription = db.scalar(
        select(Conscription).where(Conscription.boy_id == boy_id)
    )
    if not conscription:
        raise HTTPException(
            status_code=404,
            detail="Conscription record not found for this boy"
        )
    return conscription