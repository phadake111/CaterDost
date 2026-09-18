from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
import app.models as models  # Force loading models into Base metadata
from app.routes import (
    auth,
    commitments,
    dashboard,
    external_work,
    history,
    orders,
)

# Ensure tables are auto-created on Render startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CaterDost API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Included routers based on existing files in app/routes/
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(
    commitments.router, prefix="/api/v1/commitments", tags=["Commitments"]
)
app.include_router(
    dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"]
)
app.include_router(
    external_work.router,
    prefix="/api/v1/external-work",
    tags=["External Work"],
)
app.include_router(
    history.router, prefix="/api/v1/history", tags=["History"]
)


@app.get("/")
def read_root():
    return {"message": "CaterDost API is running!"}