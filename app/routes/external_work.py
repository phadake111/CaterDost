from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ExternalWork, ExternalPayment, ExternalPaymentAllocation
from app.schemas import ExternalWorkCreate, ExternalWorkOut, ExternalBulkPaymentCreate

router = APIRouter(prefix="/api/v1/external-work", tags=["External Work (Responsibility 2)"])

# 1. Record a new external shift
@router.post("", response_model=ExternalWorkOut, status_code=status.HTTP_201_CREATED)
def record_external_work(work: ExternalWorkCreate, db: Session = Depends(get_db)):
    new_work = ExternalWork(
        hired_by_name=work.hired_by_name,
        phone=work.phone,
        work_date=work.work_date,
        location=work.location,
        reach_time=work.reach_time,
        leave_time=work.leave_time,
        agreed_pay=work.agreed_pay or 0.0,
        notes=work.notes
    )
    db.add(new_work)
    db.commit()
    db.refresh(new_work)

    return ExternalWorkOut(
        id=new_work.id,
        hired_by_name=new_work.hired_by_name,
        phone=new_work.phone,
        work_date=new_work.work_date,
        location=new_work.location,
        reach_time=new_work.reach_time,
        leave_time=new_work.leave_time,
        agreed_pay=new_work.agreed_pay,
        notes=new_work.notes,
        created_at=new_work.created_at,
        total_received=0.0,
        payment_status="PENDING"
    )

# 2. Get list of all external shifts with dynamic Paid / Pending statuses
@router.get("", response_model=List[ExternalWorkOut])
def list_external_work(db: Session = Depends(get_db)):
    shifts = db.query(ExternalWork).order_by(ExternalWork.work_date.desc()).all()
    results = []

    for shift in shifts:
        total_received = sum(alloc.allocated_amount for alloc in shift.payment_allocations)
        is_paid = total_received >= (shift.agreed_pay or 0.0) and (shift.agreed_pay or 0.0) > 0

        results.append(
            ExternalWorkOut(
                id=shift.id,
                hired_by_name=shift.hired_by_name,
                phone=shift.phone,
                work_date=shift.work_date,
                location=shift.location,
                reach_time=shift.reach_time,
                leave_time=shift.leave_time,
                agreed_pay=shift.agreed_pay,
                notes=shift.notes,
                created_at=shift.created_at,
                total_received=total_received,
                payment_status="PAID" if is_paid else "PENDING"
            )
        )
    return results

# 3. Combined / Lump-Sum payment settlement
@router.post("/payments/bulk", status_code=status.HTTP_201_CREATED)
def record_combined_payment(payload: ExternalBulkPaymentCreate, db: Session = Depends(get_db)):
    """
    Handles when another caterer pays for multiple dates in a single payment.
    Example: Work A (2,000) + Work B (1,500) = 3,500 total received.
    """
    new_payment = ExternalPayment(
        payer_name=payload.payer_name,
        amount_received=payload.amount_received,
        payment_date=payload.payment_date or date.today(),
        payment_mode=payload.payment_mode or "Cash",
        notes=payload.notes
    )
    db.add(new_payment)
    db.flush()

    for item in payload.allocations:
        work_id = item.get("work_id")
        amount = item.get("amount")

        # Verify shift exists
        work_record = db.query(ExternalWork).filter(ExternalWork.id == work_id).first()
        if not work_record:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"External work record ID {work_id} not found")

        allocation = ExternalPaymentAllocation(
            payment_id=new_payment.id,
            external_work_id=work_id,
            allocated_amount=amount
        )
        db.add(allocation)

    db.commit()
    return {"message": "Payment recorded and allocated successfully", "payment_id": new_payment.id}