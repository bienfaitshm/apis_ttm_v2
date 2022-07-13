from datetime import datetime, timedelta


time = datetime(year=2022, month=7, day=14, hour=21)


week = timedelta(weeks=2)


def get_date_exp(date_dep: any):
    now = datetime.now()
    weeks_tow_diff = now + timedelta(days=14)
    hours_3_diff = now + timedelta(days=3)
    if date_dep > weeks_tow_diff:
        return now + timedelta(days=7)
    if date_dep > hours_3_diff:
        return now + timedelta(hours=12)
    return now + timedelta(hours=3)


d = get_date_exp(time)

print("date", d, time)
