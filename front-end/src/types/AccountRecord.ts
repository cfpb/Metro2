// M2 fields that can be displayed for an account record
export default interface AccountRecord {
  activity_date?: string | null
  cons_acct_num?: string | null
  port_type?: string | null
  acct_type?: string | null
  date_open?: string | null
  credit_limit?: number | null
  hcola?: number | null
  id_num?: string | null
  terms_dur?: string | null
  terms_freq?: string | null
  smpa?: number | null
  actual_pmt_amt?: number | null
  acct_stat?: string | null
  pmt_rating?: string | null
  php?: string | null
  php1?: string | null
  spc_com_cd?: string | null
  compl_cond_cd?: string | null
  current_bal?: number | null
  amt_past_due?: number | null
  orig_chg_off_amt?: number | null
  doai?: string | null
  dofd?: string | null
  date_closed?: string | null
  dolp?: string | null
  int_type_ind?: string | null
  first_name?: string | null
  surname?: string | null
  ecoa?: string | null
  ecoa_assoc?: string[] | null
  cons_info_ind?: string | null
  cons_info_ind_assoc?: string[] | null
  k2__purch_sold_ind?: string | null
  k2__purch_sold_name?: string | null
  k4__spc_pmt_ind?: string | null
  k4__deferred_pmt_st_dt?: string | null
  k4__balloon_pmt_due_dt?: string | null
  k4__balloon_pmt_amt?: string | null
  l1__change_ind?: string | null
  l1__new_acc_num?: string | null
  l1__new_id_num?: string | null
  previous_values__activity_date?: string | null
  previous_values__port_type?: string | null
  previous_values__acct_type?: string | null
  previous_values__date_open?: string | null
  previous_values__id_num?: string | null
  previous_values__acct_stat?: string | null
  previous_values__pmt_rating?: string | null
  previous_values__current_bal?: number | null
  previous_values__orig_chg_off_amt?: number | null
  previous_values__dofd?: string | null
  previous_values__date_closed?: string | null
  previous_values__first_name?: string | null
  previous_values__surname?: string | null
  previous_values__ecoa?: string | null
  previous_values__ecoa_assoc?: string | null
  previous_values__cons_info_ind?: string | null
  previous_values__cons_info_ind_assoc?: [] | null
  previous_values__l1__change_ind?: string | null
  previous_values__l1__new_acc_num?: string | null
  previous_values__l1__new_id_num?: string | null
}

// middle_name, gen_code, ssn, dob, phone_num
// addr_line_1, addr_line_2, city, state, zip, addr_ind, res_cd
