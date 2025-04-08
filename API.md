# Metro2 application API

This documentation describes the API that the Django application provides for querying all Metro2 related data.

## Authentication

Users authenticate through SSO to access the Metro2 application. After a successful login, a cookie is stored in the browser session.
All API requests will need to include that cookie in the header to successfully authenticate with the Django backend.

**Example header:**
`Cookie: csrftoken=08px9D0G8M0CSbpupDmXzm1i8zcFL6u6; sessionid=pwnfvjvonnpmvyrl732rzt6w3gszijjt`

## API endpoints

Quick links:
- [`/api/all-evaluator-metadata/`](#exporting-evaluator-metadata-csv)
- [`/api/events/{event_id}/evaluator/{evaluator_id}/csv/`](#exporting-evaluator-results-csv)
- [`/api/events/{event_id}/evaluator/{evaluator_id}/`](#evaluator-results-view)
- [`/api/events/{event_id}/accounts/{account_number}/`](#account-summary-view)
- [`/api/events/{event_id}/accounts/{account_number}/account_holder/`](#account-pii-view)
- [`/api/events/{event_id}/`](#events-view)
- [`/api/users/{user_id}/`](#users-view)

### Exporting evaluator metadata CSV

`/api/all-evaluator-metadata/`

GET - returns a CSV of evaluator metatdata from the database.

Users can export this CSV into Excel in order to sort, filter, and analyze the metadata. The CSV file name will be appended with the current date.

**Example response:**
File name: `evaluator-metadata-2024-03-18.csv`

*To do:* Update this sample response with more realistic data once eval metadata is ingested in the system.

File contents:
```csv
id,description,long_description,fields_used,fields_display,crrg_reference,potential_harm,rationale,alternate_explanation




```

### Exporting evaluator results CSV

`/api/events/{event_id}/evaluator/{evaluator_id}/csv/`

GET - returns a CSV of evaluator results for a single evaluator (whose ID matches `evaluator_id`) for a single event (with the ID `event_id`).

Users can import this CSV into Excel in order to sort, filter, and analyze the results. The CSV contains one row for each `EvaluatorResult` for the given event + evaluator combo. It has a column for each field in the "fields used" column of the Evaluator Source of Truth spreadsheet.

**Example response:**
File name: `hyundai2024_Status-DOFD.csv`

File contents:
```csv
event_name,id,activity_date,cons_acct_num,dofd,smpa,acct_stat,pmt_rating,spc_com_cd,terms_freq,current_bal,date_closed,amt_past_due,compl_cond_cd,orig_chg_off_amt
hyundai2024,1027,2019-01-31,20121204914009,,0,13,1,,M,0,2019-01-31,0,,0
hyundai2024,1100,2019-01-31,20121204941549,,0,13,1,,M,0,2019-01-29,0,,0
hyundai2024,1303,2019-01-31,20120603193654,,0,13,1,,M,0,2018-11-27,0,,0
hyundai2024,1320,2019-01-31,20121004399540,,0,13,1,,M,0,2018-11-15,0,,0
hyundai2024,1331,2019-01-31,20121205047544,,0,13,1,,M,0,2019-01-26,0,,0
```

### Evaluator results view

`/api/events/{event_id}/evaluator/{evaluator_id}/?view={sample, all}&page={x}&page_size={y}&{additional field filters}`

GET - returns a JSON with a `hits` field composed of a list that contains one object per
EvaluatorResult for a single event (with the id `event_id`) and evaluator (whose ID matches
`evaluator_id`) combo, and a `count` field that lists the count of results when paginating.

It takes a parameter, `view` parameter which can be either `sample` or `all`.
If `sample` is given then a sampling of the results that is one page long is returned.
If `all` is given, then the first page of results is returned unless `page` is given
with a page number. If `page_size` is given it will set the number of results per page,
otherwise the number of results per page will be the default sample size.

The following additional field filters can be added to the end of the query string, with
either a single value to match exactly or a comma-separated list of values to match exactly.
The special value `blank` represents an empty string to filter.

For example, the value of `acct_type` to filter for might be given in the query string as
`?acct_stat=11&view=all` or as `?acct_stat=11,13,61,62&view=all`.

- `acct_type`
- `acct_stat`
- `compl_cond_cd`
- `php`
- `pmt_rating`
- `spc_com_cd`
- `terms_freq`
- `account_holder__cons_info_ind`
- `account_holder__cons_info_ind_assoc`
- `l1__change_ind`

The following field filters can be added as either a boolean `true` or `false`.

For example, the value of `dofd` to filter for might be given in the query string as
`?dofd=true&view=all` or as `?dofd=false&view=all`.

- `dofd`
- `date_closed`

The following field filters accept value ranges.

For example, the range of of values of `amt_past_due` to filter for might be given
in the query string as `?amt_past_due_max=500&amt_past_due_min=400&view=all`.

- `amt_past_due` as `amt_past_due_max`/`amt_past_due_min`
- `current_bal` as `current_bal_max`/`current_bal_min`
- `smpa` as `smpa_max`/`smpa_min`

The keys in each EvaluatorResult object are the list of fields returned by the `result_summary_fields`
method on the EvaluatorMetadata object. (i.e. the list of fields specified in the `fields_used` column
of the SSoTS, plus a few defaults)

**Example response:**
```JSON
{
    "count": 1234,
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

`/api/events/{event_id}/accounts/{account_number}/`

GET - returns a JSON with three fields -`cons_acct_num`,`inconsistencies`, and `account_activity`. The `cons_acct_num` field contains the account number, `inconsistencies` is composed of a list of inconsistencies found for the account, and `account_activity` is composed of a list of activity records with this `cons_acct_num`.

**Example response:**
```JSON
{
    "cons_acct_num": "1234567890",
    "inconsistencies": [
        "SCC-Balance-8",
        "PROG-Bankruptcy-1",
        "Type-APD-2",
        "Balloon-Balance-1",
    ],
    "account_activity": [
        {
            "id": 3,
            "inconsistencies": [
                "SCC-Balance-8",
                "Type-APD-2",
            ],
            "activity_date": "11/30/2023",
            "account_holder__surname": "",
            "account_holder__first_name": "",
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
            "account_holder__cons_info_ind": "",
            "account_holder__ecoa": "2",
            "account_holder__cons_info_ind_assoc": ["1A", "B"],
            "account_holder__ecoa_assoc": ["2", "2", "2", "2"],
            "k2__purch_sold_ind": null,
            "k2__purch_sold_name": "",
            "k4__balloon_pmt_amt": 11854,
            "l1__change_ind": "2",
            "l1__new_id_num": "0032",
            "l1__new_acc_num": "32",
        },
        # ...etc.
    ]
}
```

### Account PII view

`/api/events/{event_id}/accounts/{account_number}/account_holder/`

GET - returns a JSON for the latest account holder information for a specified `account_number` and `event_id`.

**Example response:**
```JSON
{
    "id": 1,
    "cons_acct_num": "1234567890",
    "surname": "Claus",
    "first_name": "Santa",
    "middle_name": "H",
    "gen_code": "",
    "ssn": "333224444",
    "dob": "12/25/1900",
    "phone_num": "5552220000",
    "ecoa": "",
    "cons_info_ind": "",
    "country_cd": "",
    "addr_line_1": "12 Santa's Workshop Way",
    "addr_line_2": "",
    "city": "North Pole",
    "state": "AK",
    "zip": "99000",
    "addr_ind": "",
    "res_cd": ""
}
```

### Events view

`/api/events/{event_id}/`

GET - returns a JSON information about an event, including its name and all evaluators that have results for the specified `event_id`.

**Example response:**
```JSON
{
    "id": 1,
    "name": "Hyundai2025",
    "portfolio": "credit cards",
    "eid_or_matter_num": "123-456789",
    "other_descriptor": "",
    "directory": "Enforcement/Huyndai2025",
    "date_range_start": "2023-11-30",
    "date_range_end": "2023-12-31",
    "evaluators": [
        {
            "hits": 4209,
            "accounts_affected": 1194,
            "inconsistency_start": "2024-02-29",
            "inconsistency_end": "2024-08-29",
            "id":"DOAI-DOFD-1",
            "category": "DOFD",
            "description": "Account reports date of first delinquency longer than 7 years.",
            "long_description": "",
            "fields_used": [
                "date of first delinquency",
                "date of account information"
            ],
            "fields_display": [
                "amount past due",
                "compliance condition code",
                "current balance",
                "date closed",
                "original charge-off amount",
                "scheduled monthly payment amount",
                "special comment code",
                "terms frequency"
            ],
            "crrg_reference": "",
            "potential_harm": "",
            "rationale": "",
            "alternate_explanation": "",
        },
        # ... etc.
    ]
}

```

### Users view
If SSO is enabled:
    `/api/users/`

If SSO is not enabled:
    `/api/users/{user_id}/`

GET - returns a JSON that includes a list of all events that the user has permission to view, as well as their username and admin status

**Example response:**
```JSON
{
    "is_admin": true,
    "username": "jane.doe",
    "assigned_events": [
        {
            "id": 1,
            "name": "Hyundai2024",
            "portfolio": "credit cards",
            "eid_or_matter_num": "456-1123445",
            "other_descriptor": "",
            "date_range_start": "2023-11-30",
            "date_range_end": "2023-12-31"
        },
        # ... etc.
    ]
}
```
