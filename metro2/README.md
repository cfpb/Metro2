# Evaluators

Links to specific evaluators:
- [2_1A](#2_1A)
- [2_2A](#2_2A)
- [2_3A](#2_3A)
- [2_4A](#2_4A)
- [2_5A](#2_5A)
- [2_6A](#2_6A)
- [6_4B](#6_4B)
- [prog_dofd_1](#prog_dofd_1)
- [prog_status_1](#prog_status_1)
- [addl_apd_1](#addl_apd_1)
- [addl_doai_1](#addl_doai_1)
- [13_10B_1](#13_10B_1)
- [13_10B_2](#13_10B_2)
- [13_10B_3](#13_10B_3)
- [7_21C_1](#7_21C_1)
- [7_21C_2](#7_21C_2)
- [9_4A_1](#9_4A_1)
- [9_4A_2](#9_4A_2)
- [9_4A_3](#9_4A_3)


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

The portfolio type is not 'line of credit' (C), 'installment loan' (I), 'mortgage' (M), 'open' (O), or 'revolving' (R).

The portfolio type does not match the industry type which is either 'Bank' (B) or 'Credit Union' (CU).


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
portfolio type - Is not one of the following: C, I, O, R
industry type - Is FC

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The portfolio type is not 'line of credit' (C), 'installment loan' (I), 'open' (O), or 'revolving' (R).

The portfolio type does not match the industry type which is 'Finance Company' (FC).


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

The portfolio type is not 'line of credit' (C), 'installment loan' (I), 'mortgage' (M).

The portfolio type does not match the industry type which is 'Mortgage Lender' (M).


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

The portfolio type is not 'line of credit' (C), 'open' (O), or 'revolving' (R).

The portfolio type does not match the industry type which is 'Credit Card' (CC).


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

The portfolio type is not 'installment loan' (I), or 'revolving' (R).

The portfolio type does not match the industry type which is either 'Sales Finance' (SF) or 'Retail Store' (RS).


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

The portfolio type is not 'open' (O).

The portfolio type does not match the industry type which is either 'Collection Agency' or 'Debt Buyer' (CI).


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

The account status is not transferred (05), paid or closed / zero balance (13), paid in full - was a voluntary surrender (61), paid in full - was a collection account (62), paid in full - was a repossession (63), paid in full - was a charge-off (64), or paid in full - a foreclosure was started (65).

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

The prior account status is delinquent and is paid in full - was a voluntary surrender (61), paid in full - was a collection account (62), paid in full - was a repossession (63), paid in full - was a charge-off (64), paid in full - a foreclosure was started (65), 30-59 days past the due date (71), 60-89 days past the due date (78), 90-119 days past the due date (80), 120-149 days past the due date (82), 150-179 days past the due date (83), 180 or more days past the due date (84), assigned to internal or external collections (93), foreclosure completed; there may be a balance due (94), voluntary surrender; there may be a balance due (95), merchandise was repossessed; there may be a balance due (96), or unpaid balance reported as a loss (charge-off) (97).

The prior period's date of first delinquency is not equal to the current date of first delinquency.

The account status is delinquent and is paid in full - was a voluntary surrender (61), paid in full - was a collection account (62), paid in full - was a repossession (63), paid in full - was a charge-off (64), paid in full - a foreclosure was started (65), 30-59 days past the due date (71), 60-89 days past the due date (78), 90-119 days past the due date (80), 120-149 days past the due date (82), 150-179 days past the due date (83), 180 or more days past the due date (84), assigned to internal or external collections (93), foreclosure completed; there may be a balance due (94), voluntary surrender; there may be a balance due (95), merchandise was repossessed; there may be a balance due (96), or unpaid balance reported as a loss (charge-off) (97).

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

The prior period's account status is 30-59 days past the due date (71).

The consumer account number matches the account number from the prior month.

The prior activity date is one month prior to the current month's activity date.

The current account status is 90 or more days past the due date, either 90-119 days past the due date (80), 120-149 days past the due date (82), 150-179 days past the due date (83), or 180 days or more past the due date (84).


### addl_apd_1
#### Short description:
The account status indicates a delinquent account, but there is no amount past due.

#### Fields in output:
database record id
date created
consumer account number
account status
amount past due

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
account status - Is one of the following: '71', '78', '80', '82', '83', '84', '93', '97'
amount past due - Is zero

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The account status is either 30-59 days past the due date (71), 60-89 days past the due date (78), 90-119 days past the due date (80), 120-149 days past the due date (82), 150-179 days past the due date (83), 180 days or more past the due date (84), assigned to internal or external collections (93), or unpaid balance reported as a loss (charge-off) (97).

The amount past due is zero.


### addl_doai_1
#### Short description:
A paid or settled account status indicated but date of account information is not equal to the date of last payment.

#### Fields in output:
database record id
date created
consumer account number
account status
date of account information
date of last payment

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
account status - Is one of the following: '13', '61', '62', '63', '64', '65'
date of account information (doai) - Is not equal to date of last payment (dolp)

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The account status is either paid or closed account / zero balance (13), paid in full - was a voluntary surrender (61), paid in full - was a collection account (62), paid in full - was a repossession (63), paid in full - was a charge off (64), or paid in full - a foreclosure was started (65).

The date of account information (doai) is not equal to the date of last payment (dolp).


### 13_10B_1
#### Short description:
Account indicates a discharge for Chapter 7 or 11 bankruptcy for a charged off obligation in the base segment. But there is no date of first delinquency.

#### Fields in output:
database record id
date created
consumer account number
account status
amount past due
base consumer information indicator
current balance
date closed
date of first delinquency
scheduled monthly payment amount

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
account status - Is '97'
base consumer information indicator - Is one of the following: 'E', 'F'
date of first delinquency - There is no date of first delinquency

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The account status is unpaid balance reported as a loss (charge-off) (97).

The base consumer information indicator is either discharged through bankruptcy chapter 12 (E), or discharged through bankruptcy chapter 11 (F).

There is no date of first delinquency (dofd).


### 13_10B_2
#### Short description:
Account indicates a discharge for Chapter 7 or 11 bankruptcy for a charged off obligation in the J1 segment. But there is no date of first delinquency.

#### Fields in output:
database record id
date created
consumer account number
account status
amount past due
J1 consumer information indicator
current balance
date closed
date of first delinquency
scheduled monthly payment amount

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
database record id - Is the same between the base segment and the J1 segment
account status - Is '97'
J1 consumer information indicator - Is one of the following: 'E', 'F'
date of first delinquency - There is no date of first delinquency

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The database record id is the same between the base segment and J1 segment.

The account status is unpaid balance reported as a loss (charge-off) (97).

The J1 consumer information indicator is either discharged through bankruptcy chapter 12 (E), or discharged through bankruptcy chapter 11 (F).

There is no date of first delinquency (dofd).


### 13_10B_3
#### Short description:
Account indicates a discharge for Chapter 7 or 11 bankruptcy for a charged off obligation in the J2 segment. But there is no date of first delinquency.

#### Fields in output:
database record id
date created
consumer account number
account status
amount past due
J2 consumer information indicator
current balance
date closed
date of first delinquency
scheduled monthly payment amount

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
database record id - Is the same between the base segment and the J2 segment
account status - Is '97'
J2 consumer information indicator - Is one of the following: 'E', 'F'
date of first delinquency - There is no date of first delinquency

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The database record id is the same between the base segment and J2 segment.

The account status is unpaid balance reported as a loss (charge-off) (97).

The J2 consumer information indicator is either discharged through bankruptcy chapter 12 (E), or discharged through bankruptcy chapter 11 (F).

There is no date of first delinquency (dofd).


### 7_21C_1
#### Short description:
Special comment code suggests that the account was paid in full for less than the full balance, but the account status does not indicate the account was paid.

#### Fields in output:
database record id
date created
consumer account number
account status
amount past due
current balance
date closed
special comment code

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
account status - Is not one of the following: '13', '61', '62', '63', '64', '65'
special comment code - Is 'AU'

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The account status is not paid or closed account / zero balance (13), paid in full - was a voluntary surrender (61), paid in full - was a collection account (62), paid in full - was a repossession (63), paid in full - was a charge off (64), or paid in full - a foreclosure was started (65).

The special comment code suggests that the account was paid in full for less than the full balance (AU).


### 7_21C_2
#### Short description:
Special comment code suggests that the account was paid in full for less than the full balance, but the account status does not indicate the account was paid. Includes a K2 segment.

#### Fields in output:
database record id
date created
consumer account number
account status
amount past due
current balance
date closed
special comment code
K2 purchased - sold indicator
K2 purchased - sold name

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
database record id - The base segment id matches the id of the K2 segment
account status - Is not one of the following: '13', '61', '62', '63', '64', '65'
special comment code - Is 'AU'

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The database record id is the same between the base segment and K2 segment.

The account status is not paid or closed account / zero balance (13), paid in full - was a voluntary surrender (61), paid in full - was a collection account (62), paid in full - was a repossession (63), paid in full - was a charge off (64), or paid in full - a foreclosure was started (65).

The special comment code suggests that the account was paid in full for less than the full balance (AU).


### 9_4A_1
#### Short description:
When the account status for the previous period reported the account 30-59 days past due, the first entry of this payment history profile is not '1' which would imply that the previous period's account was 30-59 days past due. Consumer info indicator is blank in the base segment.

#### Fields in output:
database record id
date created
consumer account number
payment history profile (first character)
previous date created
previous account status
previous consumer information indicator (base segment)

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
prior account status - Is '71'
prior consumer information indicator (base segment) - Is blank
prior date created - Is one month prior to current activity date
consumer account number - Matches between the two months compared
payment history profile (first character) - Is not '1'

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The prior account status is 30-59 days past the due date (71).

The consumer information indicator is blank in the base segment.

The prior activity date is one month before the current activity date.

The consumer account number is the same between dates.

The first character of the payment history profile is not '1' which would imply that the previous period's account was 30-59 days past due.


### 9_4A_2
#### Short description:
When the account status for the previous period reported the account 30-59 days past due, the first entry of this payment history profile is not '1' which would imply that the previous period's account was 30-59 days past due. Consumer info indicator is blank in the J1 segment.

#### Fields in output:
database record id
date created
consumer account number
payment history profile (first character)
previous date created
previous account status
previous consumer information indicator (J1 segment)

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
prior account status - Is '71'
prior consumer information indicator (J1 segment) - Is blank
prior date created - Is one month prior to current activity date
consumer account number - Matches between the two months compared
payment history profile (first character) - Is not '1'

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The prior account status is 30-59 days past the due date (71).

The consumer information indicator is blank in the J1 segment.

The prior activity date is one month before the current activity date.

The consumer account number is the same between dates.

The first character of the payment history profile is not '1' which would imply that the previous period's account was 30-59 days past due.


### 9_4A_3
#### Short description:
When the account status for the previous period reported the account 30-59 days past due, the first entry of this payment history profile is not '1' which would imply that the previous period's account was 30-59 days past due. Consumer info indicator is blank in the base segment.

#### Fields in output:
database record id
date created
consumer account number
payment history profile (first character)
previous date created
previous account status
previous consumer information indicator (J2 segment)

#### Fields examined:
file - Make sure the file of the line of data matches the file of the date created field in the header
prior account status - Is '71'
prior consumer information indicator (J2 segment) - Is blank
prior date created - Is one month prior to current activity date
consumer account number - Matches between the two months compared
payment history profile (first character) - Is not '1'

#### Code description and explanation of inconsistency:
The activity date is retrieved from the file that the line of data came from.

The prior account status is 30-59 days past the due date (71).

The consumer information indicator is blank in the J2 segment.

The prior activity date is one month before the current activity date.

The consumer account number is the same between dates.

The first character of the payment history profile is not '1' which would imply that the previous period's account was 30-59 days past due.

