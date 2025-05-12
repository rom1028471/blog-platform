# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api import (
    auth_router,
    blog_router,
    post_router,
    user_router,
    image_router,
    account_router
)
from .exceptions_handlers import add_exception_handlers
from .database import engine, Base
# Импортируем модели, чтобы они зарегистрировались в метаданных
from . import models

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение всех роутеров
app.include_router(auth_router)
app.include_router(blog_router)
app.include_router(post_router)
app.include_router(user_router)
app.include_router(image_router)
app.include_router(account_router)

# Регистрация обработчиков исключений
add_exception_handlers(app)

@app.on_event("startup")
async def init_db():
    # Создание таблиц (для разработки, в продакшене используйте миграции)
    #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # Заполнение начальных данных
    from .initial_data import init_data
    from .database import SessionLocal
    db = SessionLocal()
    init_data(db)
    db.close()