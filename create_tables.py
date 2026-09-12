from app.database import engine, Base
from app.models import (
    Client, Order, OrderDay, MenuItem, OrderResource, 
    OrderHelper, OrderUtensil, OrderExpense, OrderPayment,
    ExternalWork, ExternalPayment, ExternalPaymentAllocation
)

def init_db():
    print("Creating all tables in database...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    init_db()