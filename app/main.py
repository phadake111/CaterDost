from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
import app.models as models  # Force loading models into Base metadata
from app.routes import auth, orders, items, resources, helpers

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

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(items.router, prefix="/api/v1/items", tags=["Items"])
app.include_router(resources.router, prefix="/api/v1/resources", tags=["Resources"])
app.include_router(helpers.router, prefix="/api/v1/helpers", tags=["Helpers"])

@app.get("/")
def read_root():
    return {"message": "CaterDost API is running!"}