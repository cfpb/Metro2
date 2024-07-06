import logging

from parse_m2.models import Metro2Event

############################################
# Method to update existing M2Event activity records
def update_event_records(event: Metro2Event):
    logger = logging.getLogger('parse_m2.update_event_records')
    total_updated = 0
    total_not_updated = 0
    # Retrieve Metro2Event records
    logger.info(f"Fetching all records for event: {event.name}...")
    record_set = event.get_all_account_activity()

    # Updating the records
    logger.info(f"Beginning to update all records for event: {event.name}...")
    logger.info(f"There are a total of {len(record_set)}")
    for record in record_set:
        records = record_set.filter(cons_acct_num=record.cons_acct_num).order_by("activity_date")
        # Retrieve current record index in sorted list
        record_index = list(records).index(record)
        if record_index and record_index > 0:
            record.previous_values = records[record_index-1]
            record.save()
            # count total records updated
            total_updated += 1
        else:
            # count total records not updated
            total_not_updated +=1

    logger.info(f"Previous records found and {total_updated} record{'s were' if total_updated > 1 else ' was'} updated.")
    logger.info(f"Previous records not found and {total_not_updated} record{'s were' if total_updated > 1 else ' was'} not updated.")
