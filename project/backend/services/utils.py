import datetime
from datetime import timedelta
import holidays

def is_festival_around_seven_days(festivals):
    today = datetime.today().date()
    pre_event_window = False
    post_event_window = False

    for i in range(8):  # today + next 7 days
        pre_date = today + timedelta(days=i)
        post_date = today - timedelta(days=i)
        if pre_date in holidays:
            pre_event_window = True
        if post_date in holidays:
            post_event_window = True

    return pre_event_window, post_event_window
