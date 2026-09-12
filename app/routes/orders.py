from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse, JSONResponse
from app.utils.pdf_generator import generate_client_materials_pdf


from app.database import get_db
from app.models import (
    Client, Order, OrderDay, MenuItem, OrderResource, 
    OrderHelper, OrderUtensil, OrderExpense, OrderPayment
)
from app.schemas import (
    QuickBookCreate, OrderDetailOut, MenuItemCreate, MenuItemOut,
    ResourceCreate, ResourceOut, HelperCreate, HelperOut,
    UtensilCreate, UtensilOut, ExpenseCreate, ExpenseOut,
    PaymentCreate, PaymentOut
)

router = APIRouter(prefix="/api/v1/orders", tags=["Own Orders Management"])

# --- 1. QUICK BOOKING (Designed for fast entry during client visits) ---
@router.post("/quick-book", status_code=status.HTTP_201_CREATED)
def quick_book_order(payload: QuickBookCreate, db: Session = Depends(get_db)):
    """
    Creates client (if not exists), creates basic Order, and registers Day 1.
    All completed in one atomic transaction.
    """
    # Check if client already exists by phone; if not, create new
    client = db.query(Client).filter(Client.phone == payload.client_phone).first()
    if not client:
        client = Client(name=payload.client_name, phone=payload.client_phone)
        db.add(client)
        db.flush()  # Flushes to get client.id without ending the transaction

    # Create the Order
    new_order = Order(
        client_id=client.id,
        order_title=payload.order_title,
        agreed_amount=payload.agreed_amount,
        advance_amount=payload.advance_amount,
        status="BOOKED",
        special_notes=payload.special_notes
    )
    db.add(new_order)
    db.flush()

    # Create Day 1 entry under order_days
    first_day = OrderDay(
        order_id=new_order.id,
        event_date=payload.event_date,
        event_time=payload.event_time,
        location=payload.location,
        people_count=payload.people_count,
        service_types=payload.service_types or []
    )
    db.add(first_day)

    # If advance was provided during booking, record it directly in payments table
    if payload.advance_amount and payload.advance_amount > 0:
        advance_record = OrderPayment(
            order_id=new_order.id,
            amount=payload.advance_amount,
            payment_mode="Advance / Initial",
            payment_date=date.today(),
            notes="Advance paid during booking"
        )
        db.add(advance_record)

    db.commit()
    db.refresh(new_order)

    return {
        "message": "Order booked successfully",
        "order_id": new_order.id,
        "status": new_order.status
    }


# --- 2. GET ORDER DETAILS (Full 360-degree view of an order) ---
@router.get("/{order_id}", response_model=OrderDetailOut)
def get_order_details(order_id: int, db: Session = Depends(get_db)):
    """
    Fetches the full order and dynamically calculates received and pending balances.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Dynamic money calculation: Agreed - Sum(Payments)
    total_paid = sum(p.amount for p in order.payments)
    pending_amount = max(0.0, (order.agreed_amount or 0.0) - total_paid)

    # Build the response model
    response = OrderDetailOut.model_validate(order)
    response.total_paid = total_paid
    response.pending_amount = pending_amount
    return response


# --- 3. MANUAL STATUS TOGGLE ---
@router.patch("/{order_id}/status")
def update_order_status(order_id: int, new_status: str, db: Session = Depends(get_db)):
    """
    Update status: BOOKED -> READY_FOR_EXECUTION -> COMPLETED -> CANCELLED.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    valid_statuses = ["BOOKED", "READY_FOR_EXECUTION", "COMPLETED", "CANCELLED"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid status. Must be one of {valid_statuses}"
        )

    order.status = new_status
    db.commit()
    return {"message": "Status updated successfully", "status": order.status}


# --- 4. NON-LINEAR SUB-SECTION UPDATES ---

@router.post("/{order_id}/menu", response_model=MenuItemOut, status_code=status.HTTP_201_CREATED)
def add_menu_item(order_id: int, item: MenuItemCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    new_item = MenuItem(order_id=order_id, item_name=item.item_name)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.post("/{order_id}/resources", response_model=ResourceOut, status_code=status.HTTP_201_CREATED)
def add_resource(order_id: int, res: ResourceCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    new_resource = OrderResource(
        order_id=order_id,
        resource_name=res.resource_name,
        quantity=res.quantity,
        unit=res.unit,
        is_client_provided=res.is_client_provided,
        notes=res.notes
    )
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource


@router.post("/{order_id}/helpers", response_model=HelperOut, status_code=status.HTTP_201_CREATED)
def add_helper(order_id: int, h: HelperCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    new_helper = OrderHelper(
        order_id=order_id,
        helper_name=h.helper_name,
        phone=h.phone,
        reach_time=h.reach_time,
        leave_time=h.leave_time,
        wage_amount=h.wage_amount,
        payment_status=h.payment_status or "PENDING",
        notes=h.notes
    )
    db.add(new_helper)
    db.commit()
    db.refresh(new_helper)
    return new_helper


@router.post("/{order_id}/utensils", response_model=UtensilOut, status_code=status.HTTP_201_CREATED)
def add_utensil(order_id: int, u: UtensilCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    new_utensil = OrderUtensil(
        order_id=order_id,
        item_name=u.item_name,
        quantity_sent=u.quantity_sent,
        quantity_returned=u.quantity_returned,
        notes=u.notes
    )
    db.add(new_utensil)
    db.commit()
    db.refresh(new_utensil)
    return new_utensil


@router.post("/{order_id}/payments", response_model=PaymentOut, status_code=status.HTTP_201_CREATED)
def add_payment(order_id: int, p: PaymentCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    new_payment = OrderPayment(
        order_id=order_id,
        amount=p.amount,
        payment_mode=p.payment_mode or "Cash",
        payment_date=p.payment_date or date.today(),
        notes=p.notes
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

# --- 5. LIST ORDERS (With optional status filter) ---
@router.get("", status_code=status.HTTP_200_OK)
def list_orders(status_filter: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Lists orders for the Orders tab.
    Optionally filter by status: BOOKED, READY_FOR_EXECUTION, COMPLETED.
    """
    query = db.query(Order)
    if status_filter:
        query = query.filter(Order.status == status_filter)
    
    orders = query.order_by(Order.created_at.desc()).all()
    results = []
    
    for o in orders:
        total_paid = sum(p.amount for p in o.payments)
        pending = max(0.0, (o.agreed_amount or 0.0) - total_paid)
        first_day = o.days[0] if o.days else None
        
        results.append({
            "order_id": o.id,
            "order_title": o.order_title,
            "client_name": o.client.name,
            "client_phone": o.client.phone,
            "status": o.status,
            "agreed_amount": o.agreed_amount,
            "total_paid": total_paid,
            "pending_amount": pending,
            "event_date": first_day.event_date if first_day else None,
            "people_count": first_day.people_count if first_day else 0,
            "location": first_day.location if first_day else ""
        })
    return results


# --- 6. ADD EXTRA DAYS (Multi-Day Orders: Weddings, 2-3 Day Events) ---
@router.post("/{order_id}/days", status_code=status.HTTP_201_CREATED)
def add_order_day(order_id: int, day_data: dict, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    new_day = OrderDay(
        order_id=order_id,
        event_date=day_data.get("event_date"),
        event_time=day_data.get("event_time", "11:00 AM"),
        location=day_data.get("location", ""),
        people_count=day_data.get("people_count", 0),
        service_types=day_data.get("service_types", []),
        notes=day_data.get("notes")
    )
    db.add(new_day)
    db.commit()
    db.refresh(new_day)
    return {"message": "Additional day added successfully", "day_id": new_day.id}


# --- 7. RECORD EXPENSE ---
@router.post("/{order_id}/expenses", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
def add_expense(order_id: int, exp: ExpenseCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    new_expense = OrderExpense(
        order_id=order_id,
        category=exp.category,
        description=exp.description,
        amount=exp.amount,
        expense_date=exp.expense_date or date.today(),
        notes=exp.notes
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


# --- 8. UPDATE UTENSIL RETURN COUNT ---
@router.patch("/{order_id}/utensils/{utensil_id}")
def update_utensil_return(order_id: int, utensil_id: int, quantity_returned: int, db: Session = Depends(get_db)):
    utensil = db.query(OrderUtensil).filter(
        OrderUtensil.id == utensil_id, 
        OrderUtensil.order_id == order_id
    ).first()
    if not utensil:
        raise HTTPException(status_code=404, detail="Utensil record not found")

    utensil.quantity_returned = quantity_returned
    db.commit()
    return {
        "message": "Utensil return count updated",
        "quantity_sent": utensil.quantity_sent,
        "quantity_returned": utensil.quantity_returned,
        "pending_return": max(0, utensil.quantity_sent - utensil.quantity_returned)
    }
    
@router.get("/{order_id}/pdf/client-materials")
def download_client_materials_pdf(
    order_id: int, 
    client_provided_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Streams a pure-English raw material list PDF directly to the device.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    try:
        pdf_stream = generate_client_materials_pdf(order, client_provided_only=client_provided_only)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"PDF Generation error: {str(e)}"},
            headers={"Access-Control-Allow-Origin": "*"}
        )

    filename = f"CaterDost_Materials_Order_{order_id}.pdf"

    return StreamingResponse(
        pdf_stream,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename={filename}",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )
    
# --- 10. FULL EDIT / UPDATE FOR CORE ORDER DETAILS ---
@router.put("/{order_id}")
def update_core_order(order_id: int, payload: dict, db: Session = Depends(get_db)):
    """
    Updates core order parameters: title, agreed amount, advance, notes, date, time, location, people.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update Order table fields
    if "order_title" in payload:
        order.order_title = payload["order_title"]
    if "agreed_amount" in payload:
        order.agreed_amount = float(payload["agreed_amount"])
    if "advance_amount" in payload:
        order.advance_amount = float(payload["advance_amount"])
    if "special_notes" in payload:
        order.special_notes = payload["special_notes"]

    # Update Day 1 details
    if order.days:
        day1 = order.days[0]
        if "event_date" in payload and payload["event_date"]:
            day1.event_date = payload["event_date"]
        if "event_time" in payload:
            day1.event_time = payload["event_time"]
        if "location" in payload:
            day1.location = payload["location"]
        if "people_count" in payload:
            day1.people_count = int(payload["people_count"])

    # Update Client Name / Phone if provided
    if order.client:
        if "client_name" in payload:
            order.client.name = payload["client_name"]
        if "client_phone" in payload:
            order.client.phone = payload["client_phone"]

    db.commit()
    db.refresh(order)
    return {"message": "Order details updated successfully"}


# --- 11. SUB-SECTION UPDATE & DELETE ENDPOINTS ---

# Menu Item Edit & Delete
@router.put("/{order_id}/menu/{item_id}")
def edit_menu_item(order_id: int, item_id: int, payload: MenuItemCreate, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id, MenuItem.order_id == order_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    item.item_name = payload.item_name
    db.commit()
    return {"message": "Menu item updated"}

@router.delete("/{order_id}/menu/{item_id}")
def delete_menu_item(order_id: int, item_id: int, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id, MenuItem.order_id == order_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    db.delete(item)
    db.commit()
    return {"message": "Menu item deleted"}


# Resource / Material Edit & Delete
@router.put("/{order_id}/resources/{res_id}")
def edit_resource(order_id: int, res_id: int, payload: ResourceCreate, db: Session = Depends(get_db)):
    res = db.query(OrderResource).filter(OrderResource.id == res_id, OrderResource.order_id == order_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Resource not found")
    res.resource_name = payload.resource_name
    res.quantity = payload.quantity
    res.unit = payload.unit
    res.is_client_provided = payload.is_client_provided
    res.notes = payload.notes
    db.commit()
    return {"message": "Resource updated"}

@router.delete("/{order_id}/resources/{res_id}")
def delete_resource(order_id: int, res_id: int, db: Session = Depends(get_db)):
    res = db.query(OrderResource).filter(OrderResource.id == res_id, OrderResource.order_id == order_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(res)
    db.commit()
    return {"message": "Resource deleted"}


# Helper Edit & Delete
@router.put("/{order_id}/helpers/{helper_id}")
def edit_helper(order_id: int, helper_id: int, payload: HelperCreate, db: Session = Depends(get_db)):
    h = db.query(OrderHelper).filter(OrderHelper.id == helper_id, OrderHelper.order_id == order_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Helper not found")
    h.helper_name = payload.helper_name
    h.reach_time = payload.reach_time
    h.wage_amount = payload.wage_amount
    h.payment_status = payload.payment_status or "PENDING"
    h.notes = payload.notes
    db.commit()
    return {"message": "Helper updated"}

@router.delete("/{order_id}/helpers/{helper_id}")
def delete_helper(order_id: int, helper_id: int, db: Session = Depends(get_db)):
    h = db.query(OrderHelper).filter(OrderHelper.id == helper_id, OrderHelper.order_id == order_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Helper not found")
    db.delete(h)
    db.commit()
    return {"message": "Helper deleted"}


# Utensil Delete
@router.delete("/{order_id}/utensils/{utensil_id}")
def delete_utensil(order_id: int, utensil_id: int, db: Session = Depends(get_db)):
    u = db.query(OrderUtensil).filter(OrderUtensil.id == utensil_id, OrderUtensil.order_id == order_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Utensil record not found")
    db.delete(u)
    db.commit()
    return {"message": "Utensil record deleted"}


# Payment Delete
@router.delete("/{order_id}/payments/{payment_id}")
def delete_payment(order_id: int, payment_id: int, db: Session = Depends(get_db)):
    p = db.query(OrderPayment).filter(OrderPayment.id == payment_id, OrderPayment.order_id == order_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Payment record not found")
    db.delete(p)
    db.commit()
    return {"message": "Payment record deleted"}