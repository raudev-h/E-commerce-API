from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import user, category, product, cart_item, order, auth
from core import NotFoundException, BadRequestException, ConflictException
from core.config import settings

app = FastAPI(redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail":str(exc)}
    )

@app.exception_handler(BadRequestException)
async def bad_request_handler(request, exc):
    return JSONResponse(
        content={"detail":str(exc)},
        status_code=exc.status_code
    )

@app.exception_handler(ConflictException)
async def conflict_handler(request, exc):
    return JSONResponse(
        content={"detail":str(exc)},
        status_code=exc.status_code
    )

app.include_router(user.router)
app.include_router(category.router)
app.include_router(product.router)
app.include_router(cart_item.router)
app.include_router(order.router)
app.include_router(auth.router)