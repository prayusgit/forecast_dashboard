# Default Imports
from fastapi import APIRouter
from datetime import datetime, timedelta
import holidays
from services.utils import is_festival_around_seven_days

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

@router.get('/info/{date}')
def get_is_festival(date_str: str):
    now = datetime

    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    weekday = date_obj.weekday()
    weekday = ((weekday + 1) % 7) + 1

    nepal_holidays = holidays.Nepal(years=[now.year])

    is_festival = False
    is_holiday = False
    if date_obj in nepal_holidays:
        is_festival = True

    if is_festival or weekday == 7:
        is_holiday = True

    pre_event_window, post_event_window = is_festival_around_seven_days(nepal_holidays)

    event_type = 'festival' if is_festival else 'none'
    return {
        'is_festival': is_festival,
        'is_holiday': is_holiday,
        'pre_event_window': pre_event_window,
        'post_event_window': post_event_window,
        'event_type': event_type
    }





