from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .database import init_db, async_session
from .routers import auth_router, products_router, categories_router, cart_router, orders_router
from .services.seed import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    async with async_session() as db:
        await seed_database(db)
    yield
    # Shutdown


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(products_router, prefix="/api")
app.include_router(categories_router, prefix="/api")
app.include_router(cart_router, prefix="/api")
app.include_router(orders_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "E-Commerce API", "version": "1.0.0"}


@app.get("/api/health")
async def health():
    return {"status": "ok"}
