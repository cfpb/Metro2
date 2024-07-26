import logging
from parse_m2.models import Metro2Event
from django.db import connection

############################################
# Method to update existing M2Event activity records
def post_parse(event) -> None:
    # Updating the event
    date_range = event.account_activity_date_range()
    event.date_range_start = date_range['earliest']
    event.date_range_end = date_range['latest']
    event.save()
    associate_previous_records(event)

def associate_previous_records(event: Metro2Event):
    logger = logging.getLogger('parse_m2.update_event_records')

    logger.info(f"First, make sure all previous_values pointers are empty")
    event.get_all_account_activity().update(previous_values_id=None)

    logger.info(f"Beginning to update all records for event: {event.name}")
    query_sql = """
        UPDATE "parse_m2_accountactivity" SET "previous_values_id" = prevals
        FROM (
            SELECT "parse_m2_accountactivity"."id",
            LAG ("parse_m2_accountactivity"."id", 1) OVER (
                PARTITION BY "parse_m2_accountactivity"."cons_acct_num"
                ORDER BY "parse_m2_accountactivity"."activity_date"
            ) as prevals
            FROM "parse_m2_accountactivity"
            INNER JOIN "parse_m2_accountholder" ON ("parse_m2_accountactivity"."account_holder_id" = "parse_m2_accountholder"."id")
            INNER JOIN "parse_m2_m2datafile" ON ("parse_m2_accountholder"."data_file_id" = "parse_m2_m2datafile"."id")
            WHERE "parse_m2_m2datafile"."event_id" = %s
        ) prv_lag
        WHERE prv_lag.id = parse_m2_accountactivity.id ;
    """
    with connection.cursor() as cursor:
        cursor.execute(query_sql, [event.id])

    logger.info(f"Done. Generating report...")

    record_set = event.get_all_account_activity()

    total_updated = record_set.filter(previous_values_id__isnull=False).count()
    logger.info(f"Records with a previous record associated: {total_updated}")

    total_not_updated = record_set.filter(previous_values_id__isnull=True).count()
    logger.info(f"Records with NO previous record associated: {total_not_updated}")
