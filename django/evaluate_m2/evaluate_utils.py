from django.db.models.query import QuerySet
from datetime import  date, timedelta
import calendar

class ConversionException(Exception):
    pass


def get_activity_date_range(record_set: QuerySet):
    """
    Given a query set of AccountActivity records, return the range of
    dates covered by that set of records. This returns a dict in the
    following format:
    { "earliest": date(2022, 2, 2), "latest": date(2023, 3, 3)}
    """
    earliest_date = record_set.order_by('activity_date').first().activity_date
    latest_date = record_set.order_by('-activity_date').first().activity_date
    return {"earliest": earliest_date, "latest": latest_date}

def every_month_in_range(start: date, end: date):
    """
    Given a start and end date, return a list of months in that range,
    including the start and end. This returns a list of dicts like so:
    [ {"year": 2021, "month": 11}, {"year": 2021, "month": 12},
      {"year": 2022, "month": 1}, {"year": 2022, "month": 2}, ]

    This can be used in longitudinal evaluators that need to iterate
    over all months in the data set.

    inputs:
    - start: datetime.date
    - end: datetime.date
    """
    months = []

    # Start with the first month in the range
    y = start.year
    m = start.month

    while y <= end.year:

        # If we've reached the end of the range, exit the loop
        if y >= end.year and m > end.month:
            break

        # First, add this month to the dictionary
        months.append({"year": y, "month": m})

        # Next, progress to the next month
        if m == 12:
            m = 1
            y += 1
        else:
            m += 1

    return months

def get_prior_months_by_number(activity_date: date, month_cnt=1):
    """
    Given a date activity_date, calculate the total days of the month and return the previous month.
    Throw an ConversionException if it can't be processed.

    Inputs:
    `activity_date` - the date to be compared
    """
    try:
        prev_date:date
        total_days = 0
        if month_cnt > 1:
            month = activity_date.month
            year = activity_date.year
            for i in range(0, month_cnt):
                if activity_date.month - i == 0:
                    month = 12
                    year = year - 1
                else:
                    month=month - i
                days_in_month = calendar.monthrange(year, month)[1]
                total_days = total_days + days_in_month
            prev_date=activity_date - timedelta(days=total_days)
        else:
            days_in_month = calendar.monthrange(activity_date.year, activity_date.month)[1]
            prev_date=activity_date - timedelta(days=days_in_month)
        return prev_date
    except ValueError:
        msg = f"Date value `{activity_date}` could not be converted to previous month"
        raise ConversionException(msg)
