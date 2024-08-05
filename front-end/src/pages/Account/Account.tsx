import type { AccountRecord } from 'utils/constants'

export default interface Account {
  cons_acct_num: string
  inconsistencies: string[]
  account_activity: AccountRecord[]
}
