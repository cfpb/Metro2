from django.db.models.query import QuerySet
from datetime import  date


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
