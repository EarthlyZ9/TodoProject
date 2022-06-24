import sys

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from routers.auth import get_current_user
from schemas import address_schema
from sql_app import models
from sql_app.database import SessionLocal

sys.path.append("..")

router = APIRouter(
    prefix="/address",
    tags=["Address"],
    responses={404: {"description": "Cannot find address."}},
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Add an address for user",
    response_model=address_schema.AddressOut,
)
def create_address(
    address: address_schema.AddressIn,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    address_model = models.Address()
    address_model.address1 = address.address1
    address_model.address2 = address.address2
    address_model.state = address.state
    address_model.city = address.city
    address_model.country = address.country
    address_model.zipcode = address.zipcode

    db.add(address_model)
    db.flush()  # returns id

    user = db.query(models.User).filter(models.User.id == user.get("user_id")).first()
    user.address_id = address_model.id

    db.commit()

    return address_model
