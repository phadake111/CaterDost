from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import commitments, orders,external_work, dashboard,history,auth

app = FastAPI(
    title="CaterDost API",
    description="Backend API for CaterDost - Catering Management System",
    version="1.0.0"
)

# CORS: Allows your future HTML/JS frontend to talk to this FastAPI server without browser blocking
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins during local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect modular routers
app.include_router(commitments.router)
app.include_router(orders.router)
app.include_router(external_work.router)
app.include_router(dashboard.router)
app.include_router(history.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {
        "app": "CaterDost API",
        "status": "Running",
        "docs": "/docs"
    }