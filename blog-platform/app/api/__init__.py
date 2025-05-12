# backend/app/api/__init__.py
from .auth_router import router as auth_router
from .blog_router import router as blog_router
from .post_router import router as post_router
from .user_router import router as user_router
from .image_router import router as image_router
from .account_router import router as account_router 