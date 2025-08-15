import logging
from parse_m2.models import Metro2Event
from django.db import connection

############################################
# Methods to update existing M2Event activity records
def post_parse(event) -> None:
    calculate_date_range(event)
    associate_previous_records(event)

def calculate_date_range(event: Metro2Event):
    date_range = event.account_activity_date_range()
    event.date_range_start = date_range['earliest']
    event.date_range_end = date_range['latest']
    event.save()

def associate_previous_records(event: Metro2Event):
    logger = logging.getLogger('parse_m2.associate_previous_records')

    logger.info("First, make sure all previous_values pointers are empty")
    event.get_all_account_activity().update(previous_values_id=None)

    logger.info(f"Beginning to update all records for event: {event.id}")
    query_sql = """
        UPDATE "parse_m2_accountactivity" SET "previous_values_id" = prevals
        FROM (
            SELECT "parse_m2_accountactivity"."id",
            LAG ("parse_m2_accountactivity"."id", 1) OVER (
                PARTITION BY "parse_m2_accountactivity"."cons_acct_num"
                ORDER BY "parse_m2_accountactivity"."activity_date"
            ) as prevals
            FROM "parse_m2_accountactivity"
            WHERE "parse_m2_accountactivity"."event_id" = %s
        ) prv_lag
        WHERE prv_lag.id = parse_m2_accountactivity.id ;
    """
    with connection.cursor() as cursor:
        cursor.execute(query_sql, [event.id])
