# Metro2 application API

This documentation describes the API that the Django application provides for querying all Metro2 related data.

## Authentication

TODO: Add info on how auth tokens need to be included/handled in API requests

## API endpoints

Quick links
- [`/events/{event_id}/evaluator/{evaluator_name}`](#exporting-evaluator-results)

### Exporting evaluator results

`/events/{event_id}/evaluator/{evaluator_name}`

GET - returns a CSV of evaluator results for an single evaluator (whose name matches `evaluator_name`) for a single event (with the id `event_id`).

Users can import this CSV into Excel in order to sort, filter, and analyze the results. The CSV contains one row for each `EvaluatorResult` for the given event + evaluator combo. It has a column for each field in the "fields used" column of the Evaluator Source of Truth spreadsheet.

**Example response:**
File name: `hyundai2024_ADDL-DOFD-2_12-31-2023.csv`

File contents:
```csv
event_name,id,dofd,smpa,acct_stat,pmt_rating,spc_com_cd,terms_freq,current_bal,date_closed,amt_past_due,activity_date,compl_cond_cd,cons_acct_num,orig_chg_off_amt
hyundai2024,1027,,0,13,1,,M,0,2019-01-31,0,2019-01-31,,20121204914009,0
hyundai2024,1100,,0,13,1,,M,0,2019-01-29,0,2019-01-31,,20121204941549,0
hyundai2024,1303,,0,13,1,,M,0,2018-11-27,0,2019-01-31,,20120603193654,0
hyundai2024,1320,,0,13,1,,M,0,2018-11-15,0,2019-01-31,,20121004399540,0
hyundai2024,1331,,0,13,1,,M,0,2019-01-26,0,2019-01-31,,20121205047544,0
```
