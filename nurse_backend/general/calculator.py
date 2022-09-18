from datetime import datetime
import calendar


def next_month_days():
    """
    calculate number of days in next month
    :return: a number which is total number of days next month has.
    """
    date = datetime.now().date()
    current_month = datetime.now().month
    next_month = date.replace(month=current_month + 1)
    total_days = next_month.replace(day=calendar.monthrange(next_month.year, next_month.month)[1]).day
    return total_days


def past_month_last_day():
    date = datetime.now().date()
    month = date.replace(day=calendar.monthrange(date.year, date.month)[1]).month
    date = date.replace(month=month - 1)
    date_shifted = date.replace(day=calendar.monthrange(date.year, date.month)[1])
    return date_shifted
