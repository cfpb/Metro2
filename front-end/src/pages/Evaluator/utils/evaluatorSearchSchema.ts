import { ITEMS_PER_PAGE } from '@src/constants/settings'
import { fallback } from '@tanstack/router-zod-adapter'
import { z } from 'zod'
import BooleanStringValidator from './booleanValidator'
import { listValueValidator } from './listValidator'
import minMaxValidator from './minMaxValidator'

export const evaluatorSchema = z.object({
  view: fallback(z.enum(['all', 'sample']), 'sample'),
  page: fallback(z.number().gt(0).int(), 1),
  page_size: fallback(z.number().gt(0), ITEMS_PER_PAGE),
  amt_past_due_min: minMaxValidator,
  amt_past_due_max: minMaxValidator,
  current_bal_min: minMaxValidator,
  current_bal_max: minMaxValidator,
  acct_stat: listValueValidator('acct_stat'),
  compl_cond_cd: listValueValidator('compl_cond_cd'),
  php1: listValueValidator('php1'),
  pmt_rating: listValueValidator('pmt_rating'),
  spc_com_cd: listValueValidator('spc_com_cd'),
  terms_freq: listValueValidator('terms_freq'),
  l1__change_ind: listValueValidator('l1__change_ind'),
  account_holder__cons_info_ind: listValueValidator('account_holder__cons_info_ind'),
  account_holder__cons_info_ind_assoc: listValueValidator(
    'account_holder__cons_info_ind_assoc'
  ),
  dofd: BooleanStringValidator,
  date_closed: BooleanStringValidator
})

export const evaluatorSearchSchema = evaluatorSchema.transform((params): object =>
  params.view === 'sample' ? { ...params, page: 1 } : { ...params }
)

// eslint-disable-next-line @typescript-eslint/no-type-alias
export type EvaluatorSearch = z.infer<typeof evaluatorSearchSchema>
