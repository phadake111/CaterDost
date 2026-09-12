from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, 
    ForeignKey, Text, Date, DateTime, JSON
)
from sqlalchemy.orm import relationship
from .database import Base

# --- OWN ORDERS DOMAIN ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String(120), nullable=False)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    pin = Column(String(10), nullable=False) # Simple 4-digit PIN
    created_at = Column(DateTime, default=datetime.utcnow)
    
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    phone = Column(String(20), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="client")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    order_title = Column(String(150), nullable=False)
    agreed_amount = Column(Float, default=0.0)
    advance_amount = Column(Float, default=0.0)
    status = Column(String(50), default="BOOKED")
    special_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="orders")
    days = relationship("OrderDay", back_populates="order", cascade="all, delete-orphan")
    menu_items = relationship("MenuItem", back_populates="order", cascade="all, delete-orphan")
    resources = relationship("OrderResource", back_populates="order", cascade="all, delete-orphan")
    helpers = relationship("OrderHelper", back_populates="order", cascade="all, delete-orphan")
    utensils = relationship("OrderUtensil", back_populates="order", cascade="all, delete-orphan")
    expenses = relationship("OrderExpense", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("OrderPayment", back_populates="order", cascade="all, delete-orphan")


class OrderDay(Base):
    __tablename__ = "order_days"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    event_date = Column(Date, nullable=False, index=True)
    event_time = Column(String(50), nullable=True)
    location = Column(String(255), nullable=True)
    people_count = Column(Integer, default=0)
    service_types = Column(JSON, default=list)
    notes = Column(Text, nullable=True)

    order = relationship("Order", back_populates="days")


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    item_name = Column(String(100), nullable=False)

    order = relationship("Order", back_populates="menu_items")


class OrderResource(Base):
    __tablename__ = "order_resources"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    resource_name = Column(String(100), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(30), nullable=False)
    is_client_provided = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)

    order = relationship("Order", back_populates="resources")


class OrderHelper(Base):
    __tablename__ = "order_helpers"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    helper_name = Column(String(100), nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    reach_time = Column(String(50), nullable=True)
    leave_time = Column(String(50), nullable=True)
    wage_amount = Column(Float, default=0.0)
    payment_status = Column(String(30), default="PENDING")
    notes = Column(Text, nullable=True)

    order = relationship("Order", back_populates="helpers")


class OrderUtensil(Base):
    __tablename__ = "order_utensils"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    item_name = Column(String(100), nullable=False)
    quantity_sent = Column(Integer, default=0)
    quantity_returned = Column(Integer, default=0)
    notes = Column(Text, nullable=True)

    order = relationship("Order", back_populates="utensils")


class OrderExpense(Base):
    __tablename__ = "order_expenses"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    amount = Column(Float, nullable=False)
    expense_date = Column(Date, default=date.today)
    notes = Column(Text, nullable=True)

    order = relationship("Order", back_populates="expenses")


class OrderPayment(Base):
    __tablename__ = "order_payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_mode = Column(String(50), default="Cash")
    payment_date = Column(Date, default=date.today)
    notes = Column(Text, nullable=True)

    order = relationship("Order", back_populates="payments")


# --- EXTERNAL WORK DOMAIN ---

class ExternalWork(Base):
    __tablename__ = "external_work"

    id = Column(Integer, primary_key=True, index=True)
    hired_by_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    work_date = Column(Date, nullable=False, index=True)
    location = Column(String(255), nullable=True)
    reach_time = Column(String(50), nullable=True)
    leave_time = Column(String(50), nullable=True)
    agreed_pay = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    payment_allocations = relationship("ExternalPaymentAllocation", back_populates="external_work")


class ExternalPayment(Base):
    __tablename__ = "external_payments"

    id = Column(Integer, primary_key=True, index=True)
    payer_name = Column(String(100), nullable=False)
    amount_received = Column(Float, nullable=False)
    payment_date = Column(Date, default=date.today)
    payment_mode = Column(String(50), default="Cash")
    notes = Column(Text, nullable=True)

    allocations = relationship("ExternalPaymentAllocation", back_populates="payment")


class ExternalPaymentAllocation(Base):
    __tablename__ = "external_payment_allocations"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey("external_payments.id"), nullable=False)
    external_work_id = Column(Integer, ForeignKey("external_work.id"), nullable=False)
    allocated_amount = Column(Float, nullable=False)

    payment = relationship("ExternalPayment", back_populates="allocations")
    external_work = relationship("ExternalWork", back_populates="payment_allocations")