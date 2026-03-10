from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_notification_service
from app.domain.services.notifications import NotificationService
from app.schemas.notifications import NotificationResponse

router = APIRouter()


@router.post("/consume", response_model=dict[str, int])
def consume(service: Annotated[NotificationService, Depends(get_notification_service)]) -> dict[str, int]:
    return {"processed": service.consume()}


@router.get("/users/{user_id}", response_model=list[NotificationResponse])
def list_notifications(
    user_id: str,
    service: Annotated[NotificationService, Depends(get_notification_service)],
) -> list[NotificationResponse]:
    return [
        NotificationResponse(id=item.id, recipient_user_id=item.recipient_user_id, message=item.message, status=item.status)
        for item in service.list_notifications(user_id=user_id)
    ]
