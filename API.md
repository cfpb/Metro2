# Metro2 application API

This documentation describes the API that the Django application provides for querying all Metro2 related data.

## Authentication

TODO: Add info on how auth tokens need to be included/handled in API requests

## API endpoints

Quick links:
- [`/events/{event_id}/evaluator/{evaluator_id}/csv`](#exporting-evaluator-results-csv)
- [`/events/{event_id}/evaluator/{evaluator_id}`](#evaluator-results-view)
- [`/events/{event_id}/accounts/{account_number}`](#account-summary-view)

### Exporting evaluator results CSV

`/events/{event_id}/evaluator/{evaluator_id}/csv`

GET - returns a CSV of evaluator results for a single evaluator (whose ID matches `evaluator_id`) for a single event (with the ID `event_id`).

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

### Evaluator results view

`/events/{event_id}/evaluator/{evaluator_id}`

GET - returns a JSON with a `hits` field composed of a list that contains one object per EvaluatorResult for a single event (with the id `event_id`) and evaluator (whose ID matches `evaluator_id`) combo. The keys in each object would be the list of fields saved in field_values for that EvaluatorResult.

**Example response:**
```JSON
{
    "hits": [
        {
            "id": 1026,
            "cons_acct_num": "1234567890",
            "activity_date": "1/31/2019",
            "dofd": null,
            "smpa": "0",
            "acct_stat": "13",
            "pmt_rating": "1",
            "spc_com_cd": "",
            "terms_freq": "M",
            "current_bal": 0,
            "date_closed": "11/27/2018",
            "amt_past_due": 0,
            "compl_cond_cd": null,
            "orig_chg_off_am": 0,
        }, { ... }
    ]
}
```

### Account summary view

`/events/{event_id}/accounts/{account_number}`

GET - returns a JSON with three fields -`cons_acct_num`,`inconsistencies`, and `account_activity`. The `cons_acct_num` field contains the account number, `inconsistencies` is composed of a list of inconsistencies found for the account, and `account_activity` is composed of a list of activity records with this `cons_acct_num`.

**Example response:**
```JSON
{
    "cons_acct_num": "1234567890",
    "inconsistencies": [
        {
            "id": "2",
            "name": "ADDL-DOFD-1",
        },
        # ...etc.
    ],
    "account_activity": [
        {
            "activity_date": "11/30/2023",
            "port_type": "I",
            "acct_type": "00",
            "date_open": "1/30/2018",
            "credit_limit": 0,
            "hcola": 24294,
            "terms_dur": "072",
            "terms_freq": "",
            "smpa": "",
            "actual_pmt_amt": "",
            "acct_stat": "",
            "pmt_rating": "",
            "php": "",
            "spc_com_cd": "",
            "compl_cond_cd": "",
            "current_bal": "",
            "amt_past_due": "",
            "orig_chg_off_amt": "",
            "doai": "",
            "dofd": "",
            "date_closed": "",
            "dolp": "",
            "int_type_ind": "",
        },
        # ...etc.
    ]
}
```