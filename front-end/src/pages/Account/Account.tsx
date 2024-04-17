import type { AccountRecord } from 'utils/constants'

export default interface Account {
  cons_acct_num: string
  inconsistencies: { id: string; name: string }[]
  account_activity: AccountRecord[]
}

export interface AccountHolder {
  addr_ind: string
  addr_line_1: string
  addr_line_2: string
  city: string
  cons_acct_num: string
  cons_info_ind: string
  country_cd: string
  dob: string
  ecoa: string
  first_name: string
  gen_code: string
  id: string
  middle_name: string
  phone_num: string
  res_cd: string
  ssn: string
  state: string
  surname: string
  zip: string
}
