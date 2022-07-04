from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_current_user, get_db
from app.dependencies import raise_404_error, get_authorization_exception
from app.models.address import Address
from app.models.user import User
from app.schemas import address_schema, address_user_schema, user_schema

router = APIRouter(
    prefix="/address",
    tags=["Address"],
    responses={404: {"description": "Cannot find address for the provided id."}},
)


@router.get(
    "/{address_id}",
    status_code=status.HTTP_200_OK,
    summary="Get address by id",
    response_model=address_user_schema.AddressWithUser,
    operation_id="get_address_by_id",
)
def get_address_by_id(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    address = crud.address.get(db=db, id=address_id)
    if address is None:
        raise raise_404_error(detail="Cannot find address for the provided id.")
    if address.user.id == current_user.id or crud.user.is_admin(current_user):
        return address

    raise get_authorization_exception()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get current user's address",
    response_model=address_schema.AddressOut,
    operation_id="get_address",
)
def get_address(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    if current_user.address is None:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="No address yet.")
    return current_user.address


@router.patch(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Update current user's address",
    response_model=address_user_schema.AddressWithUser,
    operation_id="update_address",
    responses={200: {"description": "Successfully updated address."}},
)
def update_address(
    new_address: address_schema.AddressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.address is None:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="No address yet.")
    address = crud.address.get(db=db, id=current_user.address_id)

    return crud.address.update(db=db, db_obj=address, obj_in=new_address)


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Delete current user's address",
    response_model=user_schema.UserWithAddress,
    operation_id="delete_address",
    responses={
        200: {"description": "Successfully delete address."},
        404: {"description": "No address to delete."},
    },
)
def delete_address(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    if current_user.address is None:
        raise raise_404_error(detail="No address to delete.")
    return crud.address.remove(db=db, id=current_user.address_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Add an address for user",
    response_model=address_user_schema.AddressWithUser,
    operation_id="create_address",
)
def create_address(
    address_in: address_schema.AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    address = crud.address.create(db=db, obj_in=address_in)

    user = crud.user.get(db=db, id=current_user.id)
    user.address_id = address.id

    db.add(user)
    db.commit()

    return address
