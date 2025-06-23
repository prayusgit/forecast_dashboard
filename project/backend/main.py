# Default Imports
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

# Module Imports
# from frontend.main import app as dash_app
from routers import info, product, category, calender

# Create FastAPI app
app = FastAPI()

# Mount Dash app under /dashboard
# app.mount("/frontend", WSGIMiddleware(dash_app.server))

# Combine the routers
app.include_router(info.router, prefix='/api/info', tags=['info'])
app.include_router(product.router, prefix='/api/product', tags=['product'])
app.include_router(category.router, prefix='/api/category', tags=['category'])
app.include_router(calender.router, prefix='/api/calender', tags=['calender'])

