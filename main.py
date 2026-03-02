from fastapi import FastAPI
from routers import user, category, product

app = FastAPI()

app.include_router(user.router)
app.include_router(category.router)
app.include_router(product.router)