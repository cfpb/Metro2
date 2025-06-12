import type AccountRecord from './AccountRecord'

export default interface Account {
  cons_acct_num: string
  inconsistencies: string[]
  account_activity: AccountRecord[]
}
