from datetime import  date, timedelta
import calendar

class ConversionException(Exception):
    pass


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
