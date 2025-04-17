const accountStatusGroups = new Map([
  ['Current', ['11']],
  ['Paid or settled in full', ['13', '61', '62', '63', '64']],
  ['Delinquent', ['71', '78', '80', '82', '83', '84', '93', '97']],
  ['Foreclosure or default', ['65', '88', '89', '94']],
  ['Repossession or surrender', ['95', '96']],
  ['Deleted', ['DA', 'DF']]
])

// const complianceConditionCodeGroups = new Map([
//   ['Account disputed', ['XB', 'XC', 'XF', 'XG', 'XH']],
//   ['Account closed', ['XA', 'XD', 'XE', 'XJ']],
//   ['Other', ['XR']]
// ])

const specialCommentCodeGroups = new Map([
  ['Transferred or sold', ['H', 'O', 'AH', 'AN', 'AT', 'BA']],
  ['Closed', ['AS', 'CI', 'CJ', 'CL', 'M']],
  ['Prepaid', ['BS']],
  ['Foreclosure', ['BO']],
  ['Forebearance', ['CP']],
  ['Lease termination', ['BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH']],
  ['Repossession or surrender', ['AO', 'AX', 'AZ', 'BH', 'BI', 'BJ', 'BK']],
  [
    'Special payment arrangements',
    ['B', 'C', 'AB', 'AC', 'AM', 'AU', 'BN', 'BP', 'BT']
  ],
  [
    'Other',
    [
      'AI',
      'AP',
      'AV',
      'AW',
      'BL',
      'CH',
      'CK',
      'CM',
      'CN',
      'CO',
      'CS',
      'DE',
      'I',
      'S',
      'V'
    ]
  ]
])

const phpCodeGroups = new Map([
  ['Current', ['0', 'E']],
  ['Delinquent', ['1', '2', '3', '4', '5', '6', 'G', 'L']],
  ['Foreclosure', ['H']],
  ['Repossession or surrender', ['J', 'K']],
  ['Other', ['B', 'D']]
])

const paymentRatingGroups = new Map([
  ['Current', ['0']],
  ['Delinquent', ['1', '2', '3', '4', '5', '6', 'G', 'L']]
])

const bankruptcyGroups = new Map([
  ['Petition for bankruptcy', ['A', 'B', 'C', 'D']],
  ['Bankruptcy discharged', ['E', 'F', 'G', 'H']],
  ['Reaffirmation of debt', ['R', 'V']],
  ['Bankruptcy indicators removed', ['Q', 'S']],
  ['Other', ['T', 'U', '1A', '2A']]
])

const termsFrequencyGroups = new Map([
  ['Deferred', ['D']],
  [
    'Not deferred (all other payment frequencies)',
    ['P', 'W', 'B', 'E', 'M', 'L', 'Q', 'T', 'S', 'Y']
  ]
])

export default {
  acct_stat: accountStatusGroups,
  php1: phpCodeGroups,
  pmt_rating: paymentRatingGroups,
  account_holder__cons_info_ind: bankruptcyGroups,
  account_holder__cons_info_ind_assoc: bankruptcyGroups,
  terms_freq: termsFrequencyGroups,
  spc_com_cd: specialCommentCodeGroups
}
