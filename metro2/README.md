# Evaluators

Links to specific evaluators:
[2_1A](#2_1A)
[2_2A](#2_2A)
[2_3A](#2_3A)
[2_4A](#2_4A)
[2_5A](#2_5A)
[2_6A](#2_6A)
[6_4B](#6_4B)
[prog_dofd_1](#prog_dofd_1)
[prog_status_1](#prog_status_1)
[addl_apd_1](#addl_apd_1)
[addl_doai_1](#addl_doai_1)
[13_10B_1](#13_10B_1)
[13_10B_2](#13_10B_2)
[13_10B_3](#13_10B_3)
[7_21C_1](#7_21C_1)
[7_21C_2](#7_21C_2)
[9_4A_1](#9_4A_1)
[9_4A_2](#9_4A_2)
[9_4A_3](#9_4A_3)


### 2_1A
#### Short description:
Portfolio type does not match the industry type, 'Bank' or 'Credit Union'

#### Fields in output:
database record id
date created
consumer account number
portfolio type

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
portfolio type - Is not one of the following: C, I, M, O, R
industry type - Is one of the following: B, CU

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The portfolio type is not 'line of credit', 'installment loan', 'mortgage', 'open', or 'revolving'.

The portfolio type does not match the industry type which is either 'Bank' or 'Credit Union'.


### 2_2A
#### Short description:
Portfolio type does not match the industry type, 'Finance Company'

#### Fields in output:
database record id
date created
consumer account number
portfolio type

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
portfolio type - Is not one of the following: C, I, M, O, R
industry type - Is FC

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The portfolio type is not 'line of credit', 'installment loan', 'open', or 'revolving'.

The portfolio type does not match the industry type which is 'Finance Company'.


### 2_3A
#### Short description:
Portfolio type does not match the industry type, 'Mortgage Lender'

#### Fields in output:
database record id
date created
consumer account number
portfolio type

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
portfolio type - Is not one of the following: C, I, M
industry type - Is M

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The portfolio type is not 'line of credit', 'installment loan', 'mortgage'.

The portfolio type does not match the industry type which is 'Mortgage Lender'.


### 2_4A
#### Short description:
Portfolio type does not match the industry type, 'Credit Card'

#### Fields in output:
database record id
date created
consumer account number
portfolio type

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
portfolio type - Is not one of the following: C, O, R
industry type - Is CC

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The portfolio type is not 'line of credit', 'open', or 'revolving'.

The portfolio type does not match the industry type which is 'Credit Card'.


### 2_5A
#### Short description:
Portfolio type does not match the industry type, 'Sales Finance' or 'Retail Store'

#### Fields in output:
database record id
date created
consumer account number
portfolio type

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
portfolio type - Is not one of the following: I, R
industry type - Is either SF or RS

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The portfolio type is not 'installment loan', or 'revolving'.

The portfolio type does not match the industry type which is either 'Sales Finance' or 'Retail Store'.


### 2_6A
#### Short description:
Portfolio type does not match the industry type, 'Collection Agency' or 'Debt Buyer'

#### Fields in output:
database record id
date created
consumer account number
portfolio type

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
portfolio type - Is not O
industry type - Is CI

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The portfolio type is not 'open'.

The portfolio type does not match the industry type which is either 'Collection Agency' or 'Debt Buyer'.


### 6_4B
#### Short description:
This is an account that has not been paid or transferred, has a current balance, and no deferred terms frequency, but has a balloon payment due date.

#### Fields in output:
database record id
date created
consumer account number
account status
terms frequency
current balance
k4 balloon payment due date

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
id - Make sure record id matches the record id of the corresponding K4 segment
accout status - Is not one of the following: '05', '13', '61', '62', '63', '64', '65'
terms frequency - Is not 'D'
current balance - Is greater than 0
K4 balloon payment due date - There is a due date

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The database record id matches the corresponding K4 segment.

The account status is not transferred, paid or closed / zero balance, paid in full - was a voluntary surrender, paid in full - was a collection account, paid in full - was a repossession, paid in full - was a charge-off, or paid in full - a foreclosure was started.

The terms frequency is not deferred.

The current balance is greater than zero.

There is a balloon payment due date.


### prog_dofd_1
#### Short description:
This period's date of first delinquency does not match the previous period when both periods had delinquent account statuses.

#### Fields in output:
database record id
date created
consumer account number
account status
date of first delinquency
previous date created
previous date of first delinquency
previous account status

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
prior account status - Is one of the following: '61', '62', '63', '64', '65', '71', '78', '80', '82', '83', '84', '93', '94', '95', '96', '97'
prior date of first delinquency - is not equal to current date of first delinquency
account status - Is one of the following: '61', '62', '63', '64', '65', '71', '78', '80', '82', '83', '84', '93', '94', '95', '96', '97'
consumer account number - Matches between periods examined
prior date created - Is one month prior to current date created

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The prior account status is delinquent and is paid in full - was a voluntary surrender, paid in full - was a collection account, paid in full - was a repossession, paid in full - was a charge-off, paid in full - a foreclosure was started, 30-59 days past the due date, 60-89 days past the due date, 90-119 days past the due date, 120-149 days past the due date, 150-179 days past the due date, 180 or more days past the due date, assigned to internal or external collections, foreclosure completed; there may be a balance due, voluntary surrender; there may be a balance due, merchandise was repossessed; there may be a balance due, or unpaid balance reported as a loss (charge-off).

The prior period's date of first delinquency is not equal to the current date of first delinquency.

The account status is delinquent and is paid in full - was a voluntary surrender, paid in full - was a collection account, paid in full - was a repossession, paid in full - was a charge-off, paid in full - a foreclosure was started, 30-59 days past the due date, 60-89 days past the due date, 90-119 days past the due date, 120-149 days past the due date, 150-179 days past the due date, 180 or more days past the due date, assigned to internal or external collections, foreclosure completed; there may be a balance due, voluntary surrender; there may be a balance due, merchandise was repossessed; there may be a balance due, or unpaid balance reported as a loss (charge-off).

The consumer account number matches between the periods examined.

The prior activity date is one month prior to the current activity date.


### prog_status_1
#### Short description:
Prior Account Status indicates that the account was 30-59 days past due, but this month's account status suggests the account is 90 or more days past due.

#### Fields in output:
database record id
date created
consumer account number
account status
previous date created
previous account status

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
prior account status - Is '71'
consumer account number - Matches the prior month's account number
prior date created - Activity date is one month prior to current month's activity date
account status - Is one of the following: '80', '82', '83', '84'

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The prior period's account status is 30-59 days past the due date.

The consumer account number matches the account number from the prior month.

The prior activity date is one month prior to the current month's activity date.

The current account status is 90 or more days past the due date, either 90-119 days past the due date, 120-149 days past the due date, 150-179 days past the due date, or 180 days or more past the due date.


### addl_apd_1
#### Short description:

#### Fields in output:

#### Fields examined:

#### Code description:

#### Description of inconsistency:

#### Location in CRRG:


### addl_doai_1
#### Short description:

#### Fields in output:

#### Fields examined:

#### Code description:

#### Description of inconsistency:

#### Location in CRRG:


### 13_10B_1
#### Short description:

#### Fields in output:

#### Fields examined:

#### Code description:

#### Description of inconsistency:

#### Location in CRRG:


### 13_10B_2
#### Short description:

#### Fields in output:

#### Fields examined:

#### Code description:

#### Description of inconsistency:

#### Location in CRRG:


### 13_10B_3
#### Short description:

#### Fields in output:

#### Fields examined:

#### Code description:

#### Description of inconsistency:

#### Location in CRRG:


### 7_21C_1
#### Short description:

#### Fields in output:

#### Fields examined:

#### Code description:

#### Description of inconsistency:

#### Location in CRRG:


### 7_21C_2
#### Short description:

#### Fields in output:

#### Fields examined:

#### Code description:

#### Description of inconsistency:

#### Location in CRRG:


### 9_4A_1
#### Short description:

#### Fields in output:

#### Fields examined:

#### Code description:

#### Description of inconsistency:

#### Location in CRRG:


### 9_4A_2
#### Short description:

#### Fields in output:

#### Fields examined:

#### Code description:

#### Description of inconsistency:

#### Location in CRRG:


### 9_4A_3
#### Short description:

#### Fields in output:

#### Fields examined:

#### Code description:

#### Description of inconsistency:

#### Location in CRRG:

