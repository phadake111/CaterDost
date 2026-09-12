from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order, OrderDay, ExternalWork, OrderUtensil, OrderPayment

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard Summary"])

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """
    Answers: What do I need to know today?
    Combines today's duties, pending alerts, and payment reminders.
    """
    today = date.today()
    next_week = today + timedelta(days=7)

    # 1. Today's Own Orders
    today_order_days = (
        db.query(OrderDay)
        .filter(OrderDay.event_date == today)
        .all()
    )
    today_own = [
        {
            "order_id": od.order.id,
            "title": od.order.order_title,
            "client_name": od.order.client.name,
            "time": od.event_time,
            "location": od.location,
            "people_count": od.people_count,
            "status": od.order.status
        }
        for od in today_order_days
    ]

    # 2. Today's External Work shifts
    today_external_shifts = (
        db.query(ExternalWork)
        .filter(ExternalWork.work_date == today)
        .all()
    )
    today_ext = [
        {
            "work_id": ew.id,
            "hired_by": ew.hired_by_name,
            "location": ew.location,
            "reach_time": ew.reach_time,
            "agreed_pay": ew.agreed_pay
        }
        for ew in today_external_shifts
    ]

    # 3. Upcoming Own Orders (Next 7 days)
    upcoming_days = (
        db.query(OrderDay)
        .filter(OrderDay.event_date > today, OrderDay.event_date <= next_week)
        .order_by(OrderDay.event_date.asc())
        .all()
    )
    upcoming_orders = [
        {
            "order_id": od.order.id,
            "title": od.order.order_title,
            "date": od.event_date,
            "people_count": od.people_count,
            "status": od.order.status
        }
        for od in upcoming_days
    ]

    # 4. Utensil Return Alerts (issued > returned)
    unreturned_utensils = (
        db.query(OrderUtensil)
        .filter(OrderUtensil.quantity_sent > OrderUtensil.quantity_returned)
        .all()
    )
    utensil_alerts = [
        {
            "order_id": u.order_id,
            "order_title": u.order.order_title,
            "client_name": u.order.client.name,
            "item_name": u.item_name,
            "missing_quantity": u.quantity_sent - u.quantity_returned
        }
        for u in unreturned_utensils
    ]

    # 5. Financial Overview: Pending balances from clients
    all_orders = db.query(Order).filter(Order.status != "COMPLETED").all()
    total_pending_client_money = 0.0
    for o in all_orders:
        paid = sum(p.amount for p in o.payments)
        total_pending_client_money += max(0.0, (o.agreed_amount or 0.0) - paid)

    return {
        "today_own_orders": today_own,
        "today_external_work": today_ext,
        "upcoming_orders": upcoming_orders,
        "utensil_alerts": utensil_alerts,
        "total_pending_client_money": total_pending_client_money
    }