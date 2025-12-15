from fastapi import APIRouter, Depends, status, HTTPException, Body
from app.services.cart_service import CartService, get_cart_service
from app.routers.auth import get_current_user
from app.models.auth import UserResponse
from app.models.cart import CartResponse

router = APIRouter()

@router.get("/", response_model=CartResponse)
async def get_cart(
    current_user: UserResponse = Depends(get_current_user),
    service: CartService = Depends(get_cart_service)
):
    return await service.get_cart(current_user.user_id)

@router.post("/items", status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    item_id: str = Body(..., embed=True),
    quantity: int = Body(1, embed=True),
    current_user: UserResponse = Depends(get_current_user),
    service: CartService = Depends(get_cart_service)
):
    await service.add_to_cart(current_user.user_id, item_id, quantity)
    return await service.get_cart(current_user.user_id)

@router.delete("/items/{item_id}")
async def remove_from_cart(
    item_id: str,
    current_user: UserResponse = Depends(get_current_user),
    service: CartService = Depends(get_cart_service)
):
    await service.remove_from_cart(current_user.user_id, item_id)
    return await service.get_cart(current_user.user_id)

@router.put("/items/{item_id}")
async def update_quantity(
    item_id: str,
    quantity: int = Body(..., embed=True),
    current_user: UserResponse = Depends(get_current_user),
    service: CartService = Depends(get_cart_service)
):
    await service.update_quantity(current_user.user_id, item_id, quantity)
    return await service.get_cart(current_user.user_id)

@router.delete("/")
async def clear_cart(
    current_user: UserResponse = Depends(get_current_user),
    service: CartService = Depends(get_cart_service)
):
    await service.clear_cart(current_user.user_id)
    return {"status": "cleared"}
