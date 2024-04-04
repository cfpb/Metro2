export default interface Account {
  cons_acct_num: string
  inconsistencies: { id: string; name: string }[]
  account_activity: Record<string, number | string>[]
}
