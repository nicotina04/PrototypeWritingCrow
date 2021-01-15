import random as rd


month_day = {4: 30, 6: 30, 11: 30, 1: 31, 3: 31, 5: 31, 7: 31, 8: 31, 9: 31, 10: 31, 12: 31}


def add_head_zero(s: str):
    if len(s) == 1:
        return '0' + s
    else:
        return s


def get_days_from_month(year: int, month: int):
    if month == 2:
        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            return 29

    try:
        return month_day[month]
    except:
        return 0


def generate_date(start_year=2020, end_year=2020, start_month=1, end_month=12):
    year = rd.randrange(start_year, end_year + 1)
    month = rd.randrange(start_month, end_month + 1)
    day = rd.randrange(1, get_days_from_month(year, month) + 1)
    hour = rd.randrange(1, 23)
    minute = rd.randrange(1, 59)
    second = rd.randrange(1, 59)

    ret = str(year) + '-' + add_head_zero(str(month)) + '-' + add_head_zero(str(day)) + ' '
    ret += add_head_zero(str(hour)) + ':' + add_head_zero(str(minute)) + ':' + add_head_zero(str(second))

    return ret


if __name__ == '__main__':
    # Test method
    for _ in range(50):
        print(generate_date())
