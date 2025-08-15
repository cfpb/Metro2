# Description: Account type does not match the portfolio type,
# Line of Credit
# Evaluator hits when both conditions are met:
# 1. port_type == 'C'
# 2. acct_type != '15', '43', '47', '89', '7A', '9B'
def eval_portfolio_type_1_func(record_set):
    return record_set \
        .filter(port_type='C') \
        .exclude(acct_type__in=['15', '43', '47', '89', '7A', '9B'])
