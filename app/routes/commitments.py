from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import OrderDay, Order, Client, ExternalWork
from app.schemas import DateCommitmentsResponse, OwnOrderCommitment, ExternalWorkCommitment

router = APIRouter(prefix="/api/v1/commitments", tags=["Date Search & Commitments"])

@router.get("", response_model=DateCommitmentsResponse)
def get_commitments_by_date(search_date: date, db: Session = Depends(get_db)):
    """
    Shows all commitments on a given date (Own Orders + External Work).
    Strict Rule: Zero financial / payment figures returned here.
    """
    # 1. Fetch Own Orders for this date
    order_days = (
        db.query(OrderDay)
        .join(Order, OrderDay.order_id == Order.id)
        .join(Client, Order.client_id == Client.id)
        .filter(OrderDay.event_date == search_date)
        .all()
    )

    own_commitments = []
    for od in order_days:
        own_commitments.append(
            OwnOrderCommitment(
                order_id=od.order.id,
                order_title=od.order.order_title,
                client_name=od.order.client.name,
                client_phone=od.order.client.phone,
                event_time=od.event_time,
                location=od.location,
                people_count=od.people_count,
                service_types=od.service_types or [],
                status=od.order.status
            )
        )

    # 2. Fetch External Work shifts for this date
    external_shifts = (
        db.query(ExternalWork)
        .filter(ExternalWork.work_date == search_date)
        .all()
    )

    ext_commitments = []
    for ew in external_shifts:
        ext_commitments.append(
            ExternalWorkCommitment(
                work_id=ew.id,
                hired_by_name=ew.hired_by_name,
                phone=ew.phone,
                location=ew.location,
                reach_time=ew.reach_time,
                leave_time=ew.leave_time
            )
        )

    return DateCommitmentsResponse(
        date=search_date,
        own_orders=own_commitments,
        external_work=ext_commitments
    )