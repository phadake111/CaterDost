from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import Client, Order, OrderHelper

router = APIRouter(prefix="/api/v1/history", tags=["History & Diary Search"])

# 1. Search Client History
@router.get("/clients")
def get_client_history(query: str, db: Session = Depends(get_db)):
    """
    Search by client name or phone to see all past orders.
    Replaces flipping through old diary pages.
    """
    clients = (
        db.query(Client)
        .filter((Client.name.ilike(f"%{query}%")) | (Client.phone.ilike(f"%{query}%")))
        .all()
    )
    
    results = []
    for c in clients:
        orders_data = []
        for o in c.orders:
            first_day = o.days[0] if o.days else None
            orders_data.append({
                "order_id": o.id,
                "order_title": o.order_title,
                "status": o.status,
                "agreed_amount": o.agreed_amount,
                "date": first_day.event_date if first_day else None,
                "people_count": first_day.people_count if first_day else 0
            })
        results.append({
            "client_id": c.id,
            "name": c.name,
            "phone": c.phone,
            "total_orders": len(c.orders),
            "orders": orders_data
        })
    return results

# 2. Search Helper Work History
@router.get("/helpers")
def get_helper_history(name: str, db: Session = Depends(get_db)):
    """
    Search helper name (e.g., 'Ramesh') to see all orders they worked on, 
    dates, wages, and payment statuses.
    """
    records = (
        db.query(OrderHelper)
        .filter(OrderHelper.helper_name.ilike(f"%{name}%"))
        .all()
    )
    
    history = []
    total_earned = 0.0
    total_pending = 0.0

    for r in records:
        order = r.order
        first_day = order.days[0] if order.days else None
        wage = r.wage_amount or 0.0
        total_earned += wage
        if r.payment_status == "PENDING":
            total_pending += wage

        history.append({
            "order_id": order.id,
            "order_title": order.order_title,
            "event_date": first_day.event_date if first_day else None,
            "reach_time": r.reach_time,
            "leave_time": r.leave_time,
            "wage_amount": wage,
            "payment_status": r.payment_status,
            "notes": r.notes
        })

    return {
        "helper_name": name,
        "total_shifts": len(records),
        "total_earned": total_earned,
        "total_pending_wages": total_pending,
        "work_history": history
    }