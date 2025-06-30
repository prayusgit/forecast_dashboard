# Default Imports
from fastapi import APIRouter
from datetime import datetime, timedelta
import holidays


router = APIRouter()


@router.get('/festivals_within_7_days')
def get_festivals():
    now = datetime.today().date()

    nepal_holidays = holidays.Nepal(years=[now.year, now.year+1])

    festivals = {}

    for key, value in nepal_holidays.items():
        if 1 <= (key - now).days <= 7:
            festivals[value] = key
    return festivals

