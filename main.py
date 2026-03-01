from fastapi import FastAPI
from routers import user, category

app = FastAPI()

app.include_router(user.router)
app.include_router(category.router)