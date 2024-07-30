from datetime import  date
import re

from django.db.models.query import QuerySet


def get_activity_date_range(record_set: QuerySet):
    """
    Given a query set of AccountActivity records, return the range of
    dates covered by that set of records. This returns a dict in the
    following format:
    { "earliest": date(2022, 2, 2), "latest": date(2023, 3, 3)}
    """
    if record_set.exists():
        earliest_date = record_set.order_by('activity_date').first().activity_date
        latest_date = record_set.order_by('-activity_date').first().activity_date
        return {"earliest": earliest_date, "latest": latest_date}
    else:
        return {"earliest": None, "latest": None}

def create_eval_insert_query(eval_query: str, result_summary) -> str:
    rx = re.compile('SELECT .* FROM \"parse_m2_accountactivity\"')

    desired_fields = ",".join(["parse_m2_accountactivity.id",
                      "parse_m2_accountactivity.activity_date",
                      "parse_m2_accountactivity.cons_acct_num",
                      str(result_summary.id)])

    select_query, success = rx.subn(f"SELECT {desired_fields} FROM parse_m2_accountactivity", eval_query)
    if success != 1:
        raise TypeError

    insert_query = """
        INSERT into evaluate_m2_evaluatorresult
            (source_record_id, date, acct_num, result_summary_id)
    """
    return insert_query + select_query

def get_activity_date_range_from_list(data: list[dict]):
    """
    Given a list of dictionary, return the range of
    dates covered by that set of records. This returns a dict in the
    following format:
    { "earliest": date(2022, 2, 2), "latest": date(2023, 3, 3)}
    """
    activity_date_list = list(d['activity_date'] for d in data)
    activity_date_list.sort()
    earliest_date = activity_date_list[0]
    latest_date = activity_date_list[-1]
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
