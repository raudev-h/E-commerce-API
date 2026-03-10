from fastapi import FastAPI
from routers import user, category, product, cart_item

app = FastAPI()

app.include_router(user.router)
app.include_router(category.router)
app.include_router(product.router)
app.include_router(cart_item.router)