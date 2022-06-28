import sys

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from routers.auth import get_current_user
from schemas import address_schema, address_user_schema
from todo_proj import models
from todo_proj.database import SessionLocal
from todo_proj.dependencies import raise_404_error

sys.path.append("..")

router = APIRouter(
    prefix="/address",
    tags=["Address"],
    responses={404: {"description": "Cannot find address for the provided id."}},
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get(
    "/{address_id}",
    status_code=status.HTTP_200_OK,
    summary="Get address by id",
    response_model=address_user_schema.AddressWithUser,
    responses={404: {"description": "Cannot find address for the provided id."}},
)
def get_address(address_id: int, db: Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if address is None:
        raise raise_404_error(detail="Cannot find address for the provided id.")
    return address


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Add an address for user",
    response_model=address_user_schema.AddressOut,
)
def create_address(
    address: address_schema.AddressIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    address_model = models.Address(**address.dict())
    # address_model.address1 = address.address1
    # address_model.address2 = address.address2
    # address_model.state = address.state
    # address_model.city = address.city
    # address_model.country = address.country
    # address_model.zipcode = address.zipcode

    db.add(address_model)
    db.flush()  # returns id

    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    user.address_id = address_model.id
    user.address = address_model
    db.add(user)

    db.commit()

    return address_model
