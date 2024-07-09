import logging
from django.db.models import Window
from django.db.models.functions import Lag

############################################
# Method to update existing M2Event activity records
def associate_previous_records(event):
    logger = logging.getLogger('parse_m2.update_event_records')

    # Updating the records
    logger.info(f"Beginning to update all records for event: {event.name}...")

    # Retrieve Metro2Event records
    record_set = event.get_all_account_activity()

    # For each record in the set, find the id of the previous record for that account
    # num, ordered by activity date. Assign the previous record ID to a field called 'prevals'.
    result = record_set.annotate(prevals=Window(
        expression=Lag("id"),
        partition_by="cons_acct_num",
        order_by="activity_date"
    ),)

    # For each record, assign the 'prevals' id as the previous_values_id
    for r in result:
        r.previous_values_id=r.prevals

    # Save the new value for all records
    record_set.bulk_update(result, ["previous_values_id"])

    # Calculate how many were updated
    total_not_updated = record_set.filter(previous_values_id__isnull=True).count()
    total_updated = record_set.filter(previous_values_id__isnull=False).count()

    logger.info(f"Previous records found and {total_updated} record{'s were' if total_updated > 1 else ' was'} updated.")
    logger.info(f"Previous records not found and {total_not_updated} record{'s were' if total_updated > 1 else ' was'} not updated.")