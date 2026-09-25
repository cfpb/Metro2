import logging

from django.db import connection

from parse_m2.models import Metro2Event


############################################
# Methods to update existing M2Event activity records
def post_parse(event) -> None:
    logger = logging.getLogger('parse_m2.post_parse')
    logger.info("Calculating total records.")
    save_total_records(event)
    logger.info("Calculating event date range.")
    save_date_range(event)
    logger.info("Beginning progressive evaluator query.")
    associate_previous_records(event)

def save_date_range(event: Metro2Event):
    date_range = event.account_activity_date_range()
    event.date_range_start = date_range['earliest']
    event.date_range_end = date_range['latest']
    event.save()

def save_total_records(event: Metro2Event):
    event.total_tradelines = event.calculate_total_tradelines()
    event.save()

def _create_previous_values_temp_table(event_id):
    create_temp_table_query = """
        CREATE table temp_previous_values_for_event as (
            SELECT "parse_m2_accountactivity"."id",
            LAG ("parse_m2_accountactivity"."id", 1) OVER (
                PARTITION BY "parse_m2_accountactivity"."cons_acct_num"
                ORDER BY "parse_m2_accountactivity"."activity_date"
            ) as prev_vals
            FROM "parse_m2_accountactivity"
            WHERE "parse_m2_accountactivity"."event_id" = %s
        )
    """
    with connection.cursor() as cursor:
        cursor.execute(create_temp_table_query, [event_id])

def _create_previous_values_index():
    temp_table_index_sql = """
        CREATE INDEX idx_tmp_accountactivity_id
        ON temp_previous_values_for_event (id)
    """
    with connection.cursor() as cursor:
        cursor.execute(temp_table_index_sql)

def _write_previous_values_to_account_activity():
    update_previous_values_sql = """
        UPDATE "parse_m2_accountactivity"
        SET "previous_values_id" = prev_vals
        FROM "temp_previous_values_for_event"
        WHERE "temp_previous_values_for_event"."id" = parse_m2_accountactivity.id
    """
    with connection.cursor() as cursor:
        cursor.execute(update_previous_values_sql)

def _clean_up_temp_table():
    delete_temp_table_sql = """
        drop table temp_previous_values_for_event
    """
    with connection.cursor() as cursor:
        cursor.execute(delete_temp_table_sql)

def associate_previous_records(event: Metro2Event):
    """
    a.k.a. "the progressive evaluator query"
    """
    logger = logging.getLogger('parse_m2.associate_previous_records')

    all_records = event.get_all_account_activity()
    # if all_records.filter(previous_values_id__isnull=False).exists():
    #     logger.info("First, make sure all previous_values pointers are empty.")
    #     all_records.update(previous_values_id=None)

    logger.info("Creating temp table of previous values...")
    _create_previous_values_temp_table(event.id)

    # logger.info("Creating index...")
    # _create_previous_values_index()

    logger.info("Updating AccountActivity...")
    _write_previous_values_to_account_activity()

    logger.info("Done. Cleaning up...")
    _clean_up_temp_table()

