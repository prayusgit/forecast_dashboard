# Default Imports
from fastapi import APIRouter
from datetime import datetime, timedelta

router = APIRouter()


@router.get('/festivals_within_7_days')
def get_festivals():
    festivals = {
        "Asar 15": datetime(2025, 6, 30).date(),
        "Eid al-Adha": datetime(2025, 6, 25).date(),
        "Teej": datetime(2025, 8, 28).date()
    }
    return festivals

