import logging

from django.db import connection

from parse_m2.models import M2DataFile, Metro2Event


############################################
# Methods to update existing M2Event activity records
def post_parse(event: Metro2Event, strategy:str = 'chunk') -> None:
    logger = logging.getLogger('parse_m2.post_parse')
    logger.info("Calculating total records.")
    save_total_records(event)
    if event.total_tradelines > 0:
        logger.info("Calculating event date range.")
        save_date_range(event)
        logger.info("Beginning progressive evaluator query.")
        associate_previous_records(event, strategy)
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

def associate_previous_records(event: Metro2Event, strategy: str = 'chunk'):
    """
    For each applicable record, set previous_values to the record
    with the same consumer account number and the closest earlier
    activity date. (a.k.a. 'the progressive evaluator query')
    Since this is a complex and time-consuming task, there are three
    possible strategies to accomplish it. The strategy field should
    match one of these options: lag, chunk, file. Also accepts 'skip'
    option to skip associating prior records at all.
    See code comments for details of how each strategy works and when to use it.
    """
    logger = logging.getLogger('parse_m2.associate_previous_records')
    if strategy == 'file':
        logger.info("Using the datafile strategy to associate prior records.")
        associate_prior_records_by_file_order(event)
    elif strategy[:5] == 'chunk':
        logger.info("Using the chunk strategy to associate prior records.")
        try:
            chunk_size = int(strategy[5:])
            chunk_method_associate_prior_records(event, chunk_size)
        except ValueError:
            chunk_method_associate_prior_records(event)
    elif strategy == 'lag':
        logger.info("Using the lag strategy to associate prior records.")
        lag_method_associate_prior_records(event)
    elif strategy == 'skip':
        logger.info("'Skip' option, was used; skipping prior records step.")
    else:
        logger.info(
            f"Invalid strategy input: {strategy}. "
            "Must match one of the following: lag, chunk, file, or skip")

def report_on_prior_record_outcome(event: Metro2Event):
    logger = logging.getLogger('parse_m2.report_on_prior_record_outcome')

    record_set = event.get_all_account_activity()
    total_updated = record_set.filter(previous_values_id__isnull=False).count()
    logger.info(f"Records with a previous record associated: {total_updated:,}")
    total_not_updated = record_set.filter(previous_values_id__isnull=True).count()
    logger.info(f"Records with NO previous record associated: {total_not_updated:,}")

    event.prior_records_associated = total_updated
    event.save()


# Lag strategy for associating prior records
##########################################################################
# This strategy processes the whole dataset at once. This is preferred when
# the dataset is small.
# For each consumer account, put all of the records in order by activity date,
# then assign previous_values based on that order.
def lag_method_associate_prior_records(event: Metro2Event):
    logger = logging.getLogger('parse_m2.lag_method_associate_prior_records')
    query_sql = """
        UPDATE parse_m2_accountactivity SET previous_values_id = prevals
        FROM (
            SELECT id, LAG (id, 1) OVER (
                PARTITION BY cons_acct_num ORDER BY activity_date
            ) as prevals
            FROM parse_m2_accountactivity
            WHERE event_id = %s
        ) prv_lag
        WHERE prv_lag.id = parse_m2_accountactivity.id;
    """
    with connection.cursor() as cursor:
        logger.info("Beginning to associate previous values...")
        cursor.execute(query_sql, [event.id])


# Chunk strategy for associating prior records
##########################################################################
# Uses the same basic method as the lag strategy, but splits the dataset
# into smaller transactions of chunk_size accounts. Choose this strategy
# for larger datasets where we can't can't use the file strategy (below),
# since we don't know the cadence of how often individual accounts are reported.
def chunk_method_associate_prior_records(event: Metro2Event, chunk_size = 100_000):
    logger = logging.getLogger('parse_m2.chunk_method_associate_prior_records')
    # Count the number of distinct account numbers
    total_accts = event.accountactivity_set.values('cons_acct_num').distinct().count()

    # Use that to decide number of chunks
    q,r = divmod(total_accts, chunk_size)
    num_chunks = q + (1 if r else 0)
    logger.info("Associating previous values using chunks of "
            f"{chunk_size:,} accounts. For {total_accts:,}, using "
            f"{num_chunks:,} total chunks.")

    # Run the query on each chunk
    for i in range(num_chunks):
        _update_one_chunk(event.id, i, chunk_size)

def _update_one_chunk(event_id: int, chunk_counter: int, chunk_size: int):
    logger = logging.getLogger('parse_m2.chunk_method_associate_prior_records')
    # do the lag function on a set of chunk_size accounts
    query_sql = """
        UPDATE parse_m2_accountactivity SET previous_values_id = prevals
        FROM (
            SELECT id, LAG (id, 1) OVER (
                PARTITION BY cons_acct_num ORDER BY activity_date
            ) as prevals
            FROM parse_m2_accountactivity
            WHERE event_id = %s
            AND cons_acct_num in (
                SELECT DISTINCT cons_acct_num from parse_m2_accountactivity
                WHERE event_id = %s
                ORDER BY cons_acct_num
                LIMIT %s OFFSET %s
            )
        ) prv_lag
        WHERE prv_lag.id = parse_m2_accountactivity.id;
    """
    offset = chunk_size * chunk_counter
    with connection.cursor() as cursor:
        logger.info(f"Associating previous values for chunk #{chunk_counter + 1}...")
        cursor.execute(query_sql, [event_id, event_id, chunk_size, offset])


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
