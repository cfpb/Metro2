from datetime import  date, timedelta
import calendar

class ConversionException(Exception):
    pass


def get_previous_month(activity_date: date):
    """
    Given a date activity_date, calculate the total days of the month and return the previous month. Throw an UnreadableLineException
    if it can't be processed.

    Inputs:
    `activity_date` - the date to be compared
    """
    try:
        days_in_month = calendar.monthrange(activity_date.year, activity_date.month)[1]
        prev_date=activity_date - timedelta(days=days_in_month)

        return prev_date
    except ValueError:
        msg = f"Date value `{activity_date}` could not be converted to previous month"
        raise ConversionException(msg)
