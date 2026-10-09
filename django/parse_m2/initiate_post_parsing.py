import logging

from django.db import connection

from parse_m2.models import M2DataFile, Metro2Event


############################################
# Methods to update existing M2Event activity records
def post_parse(event, file_strategy=False) -> None:
    logger = logging.getLogger('parse_m2.post_parse')
    logger.info("Calculating total records.")
    save_total_records(event)
    if event.total_tradelines > 0:
        logger.info("Calculating event date range.")
        save_date_range(event)
        logger.info("Beginning progressive evaluator query.")
        associate_previous_records(event, file_strategy)
        logger.info("Done. Generating report...")
        report_on_prior_record_outcome(event)
    else:
        logger.info("No tradelines found.")


def save_date_range(event: Metro2Event):
    date_range = event.account_activity_date_range()
    event.date_range_start = date_range['earliest']
    event.date_range_end = date_range['latest']
    event.save()

def save_total_records(event: Metro2Event):
    event.total_tradelines = event.calculate_total_tradelines()
    event.save()

def associate_previous_records(event: Metro2Event, file_strategy: bool=False):
    """ a.k.a. 'the progressive evaluator query' """
    logger = logging.getLogger('parse_m2.associate_previous_records')
    if file_strategy:
        logger.info("Using the datafile strategy to associate prior records.")
        associate_prior_records_by_file_order(event)
    else:
        logger.info("Using the lag strategy to associate prior records.")
        lag_method_associate_prior_records(event)

def report_on_prior_record_outcome(event: Metro2Event):
    logger = logging.getLogger('parse_m2.report_on_prior_record_outcome')

    record_set = event.get_all_account_activity()
    total_updated = record_set.filter(previous_values_id__isnull=False).count()
    logger.info(f"Records with a previous record associated: {total_updated}")
    total_not_updated = record_set.filter(previous_values_id__isnull=True).count()
    logger.info(f"Records with NO previous record associated: {total_not_updated}")

    event.prior_records_associated = total_updated
    event.save()


# Lag strategy for associating prior records
##########################################################################
# Also known as the 'lag' strategy, this processes the whole dataset at once.
# This strategy is preferred when the dataset is small, and when we can't
# assume the accounts are reported monthly.
# For each consumer account, put all of the records in order by activity date,
# then assign previous_values based on that order.
def lag_method_associate_prior_records(event: Metro2Event):
    logger = logging.getLogger('parse_m2.lag_method_associate_prior_records')
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
        logger.info("Beginning to associate previous values...")
        cursor.execute(query_sql, [event.id])
        logger.info("Done.")


# Data file strategy for associating prior records
##########################################################################
# This is the preferred strategy for associating prior records for large datasets,
# if the data structure allows. If we believe accounts are reported once per month
# and the files are separated by collection, use the 'previous_file' value on
# the M2DataFile to indicate where to look for prior records.
def _associate_prior_records_single_datafile(
    file_to_update: M2DataFile,
    prior_file: M2DataFile
):
    query_sql = """
        UPDATE parse_m2_accountactivity SET previous_values_id = prev_id
        from (
            SELECT cons_acct_num, id as prev_id
            FROM parse_m2_accountactivity
            WHERE parse_m2_accountactivity.data_file_id = %s
        ) prv_records
        WHERE parse_m2_accountactivity.cons_acct_num = prv_records.cons_acct_num
        AND parse_m2_accountactivity.data_file_id = %s ;
    """
    with connection.cursor() as cursor:
        cursor.execute(query_sql, [prior_file.id, file_to_update.id])

def associate_prior_records_by_file_order(event: Metro2Event):
    logger = logging.getLogger('parse_m2.associate_prior_records_by_file_order')
    for f in event.m2datafile_set.order_by('activity_date'):
        if f.previous_file:
            logger.info(f"Assigning prior records for `{f.file_name}`"
                        f" from `{f.previous_file.file_name}.")
            _associate_prior_records_single_datafile(f, f.previous_file)
        else:
            logger.info(f"{f.file_name} does not have a 'prior' file.")
