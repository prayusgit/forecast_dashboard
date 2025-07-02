# Default Imports
from fastapi import APIRouter
import pandas as pd
from datetime import datetime
import os

# Module Imports
from services.data_loader import load_transaction_data
from services.model import load_model

router = APIRouter()

df = load_transaction_data()

category_to_products = (
        df.groupby('category')['product']
        .unique()
        .apply(list)
        .to_dict()
    )


@router.get('/categories')
def get_categories():
    categories = list(category_to_products.keys())
    return {'categories': categories}


@router.get('/products')
def get_products():
    all_products = [product for products in category_to_products.values() for product in products]
    return {'products': all_products}


@router.get('/category_to_products/{category}')
def get_products(category: str):
    return {'products': category_to_products[category]}

