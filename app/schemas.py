from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

# --- BASE / SHARED SCHEMAS ---

class ClientBase(BaseModel):
    name: str
    phone: str

class ClientCreate(ClientBase):
    pass

class ClientOut(ClientBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- QUICK BOOKING SCHEMAS ---

class QuickBookCreate(BaseModel):
    client_name: str
    client_phone: str
    order_title: str
    event_date: date
    event_time: Optional[str] = "11:00 AM"
    location: Optional[str] = ""
    people_count: Optional[int] = 0
    service_types: Optional[List[str]] = []
    agreed_amount: Optional[float] = 0.0
    advance_amount: Optional[float] = 0.0
    special_notes: Optional[str] = None

# --- SUB-SECTION SCHEMAS (OWN ORDERS) ---

class MenuItemCreate(BaseModel):
    item_name: str

class MenuItemOut(MenuItemCreate):
    id: int
    order_id: int
    model_config = ConfigDict(from_attributes=True)

class ResourceCreate(BaseModel):
    resource_name: str
    quantity: float
    unit: str
    is_client_provided: bool = False
    notes: Optional[str] = None

class ResourceOut(ResourceCreate):
    id: int
    order_id: int
    model_config = ConfigDict(from_attributes=True)

class HelperCreate(BaseModel):
    helper_name: str
    phone: Optional[str] = None
    reach_time: Optional[str] = None
    leave_time: Optional[str] = None
    wage_amount: Optional[float] = 0.0
    payment_status: Optional[str] = "PENDING"
    notes: Optional[str] = None

class HelperOut(HelperCreate):
    id: int
    order_id: int
    model_config = ConfigDict(from_attributes=True)

class UtensilCreate(BaseModel):
    item_name: str
    quantity_sent: int = 0
    quantity_returned: int = 0
    notes: Optional[str] = None

class UtensilOut(UtensilCreate):
    id: int
    order_id: int
    model_config = ConfigDict(from_attributes=True)

class ExpenseCreate(BaseModel):
    category: str
    description: Optional[str] = None
    amount: float
    expense_date: Optional[date] = None
    notes: Optional[str] = None

class ExpenseOut(ExpenseCreate):
    id: int
    order_id: int
    model_config = ConfigDict(from_attributes=True)

class PaymentCreate(BaseModel):
    amount: float
    payment_mode: Optional[str] = "Cash"
    payment_date: Optional[date] = None
    notes: Optional[str] = None

class PaymentOut(PaymentCreate):
    id: int
    order_id: int
    model_config = ConfigDict(from_attributes=True)

class OrderDayOut(BaseModel):
    id: int
    event_date: date
    event_time: Optional[str]
    location: Optional[str]
    people_count: int
    service_types: List[str]
    notes: Optional[str]
    model_config = ConfigDict(from_attributes=True)

# --- DETAILED ORDER OUTPUT ---

class OrderDetailOut(BaseModel):
    id: int
    client: ClientOut
    order_title: str
    agreed_amount: float
    advance_amount: float
    status: str
    special_notes: Optional[str]
    created_at: datetime
    
    # Nested arrays
    days: List[OrderDayOut] = []
    menu_items: List[MenuItemOut] = []
    resources: List[ResourceOut] = []
    helpers: List[HelperOut] = []
    utensils: List[UtensilOut] = []
    expenses: List[ExpenseOut] = []
    payments: List[PaymentOut] = []
    
    # Computed balances
    total_paid: float = 0.0
    pending_amount: float = 0.0

    model_config = ConfigDict(from_attributes=True)

# --- EXTERNAL WORK SCHEMAS ---

class ExternalWorkCreate(BaseModel):
    hired_by_name: str
    phone: Optional[str] = None
    work_date: date
    location: Optional[str] = None
    reach_time: Optional[str] = None
    leave_time: Optional[str] = None
    agreed_pay: Optional[float] = 0.0
    notes: Optional[str] = None

class ExternalWorkOut(ExternalWorkCreate):
    id: int
    created_at: datetime
    total_received: float = 0.0
    payment_status: str = "PENDING"  # PAID or PENDING
    model_config = ConfigDict(from_attributes=True)

class ExternalBulkPaymentCreate(BaseModel):
    payer_name: str
    amount_received: float
    payment_mode: Optional[str] = "Cash"
    payment_date: Optional[date] = None
    notes: Optional[str] = None
    # Allocation mapping: list of {work_id: int, amount: float}
    allocations: List[dict]

# --- DATE SEARCH (COMMITMENTS) SCHEMAS ---
# Strictly NO PRICING to respect CaterDost UX rules

class OwnOrderCommitment(BaseModel):
    order_id: int
    order_title: str
    client_name: str
    client_phone: str
    event_time: Optional[str]
    location: Optional[str]
    people_count: int
    service_types: List[str]
    status: str

class ExternalWorkCommitment(BaseModel):
    work_id: int
    hired_by_name: str
    phone: Optional[str]
    location: Optional[str]
    reach_time: Optional[str]
    leave_time: Optional[str]

class DateCommitmentsResponse(BaseModel):
    date: date
    own_orders: List[OwnOrderCommitment]
    external_work: List[ExternalWorkCommitment]