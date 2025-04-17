import { fallback } from '@tanstack/router-zod-adapter'
import { z } from 'zod'

import { M2_FIELD_LOOKUPS } from 'utils/annotationLookups'
import { ITEMS_PER_PAGE } from '../EvaluatorUtils'

/**
 * Validation for an optional number in search params.
 *
 * The empty string fallback is used because it causes
 * Tanstack router to remove the parameter
 * from the query string if its value is invalid.
 */
export const minMaxParser = fallback(
  z.union([z.number(), z.enum([''])]).optional(),
  ''
)

export const validateFieldValues = (
  val: unknown,
  field: keyof typeof M2_FIELD_LOOKUPS
): string[] => {
  const arr = Array.isArray(val) ? val : [val]
  const lookup = M2_FIELD_LOOKUPS[field]
  // eslint-disable-next-line @typescript-eslint/no-unsafe-return
  return arr
    .filter(item => item in lookup || Number(item) in lookup || item === 'blank')
    .map(String)
}

export const listValueParser = (
  field: keyof typeof M2_FIELD_LOOKUPS
): z.ZodOptional<z.ZodEffects<z.ZodAny, string[], unknown>> =>
  z
    .any()
    .transform(val => validateFieldValues(val, field))
    .optional()

export const schema = z.object({
  view: fallback(z.enum(['all', 'sample']), 'sample'),
  page: fallback(z.number().gt(0), 1),
  page_size: fallback(z.number().gt(0), ITEMS_PER_PAGE),
  amt_past_due_min: minMaxParser,
  amt_past_due_max: minMaxParser,
  current_bal_min: minMaxParser,
  current_bal_max: minMaxParser,
  acct_stat: listValueParser('acct_stat'),
  compl_cond_cd: listValueParser('compl_cond_cd'),
  php1: listValueParser('php1'),
  pmt_rating: listValueParser('pmt_rating'),
  spc_com_cd: listValueParser('spc_com_cd'),
  terms_freq: listValueParser('terms_freq'),
  l1__change_ind: listValueParser('l1__change_ind'),
  account_holder__cons_info_ind: listValueParser('account_holder__cons_info_ind'),
  account_holder__cons_info_ind_assoc: listValueParser(
    'account_holder__cons_info_ind_assoc'
  )
})

export const evaluatorSearchSchema = schema.transform((params): object =>
  params.view === 'sample' ? { ...params, page: 1 } : { ...params }
)

// eslint-disable-next-line @typescript-eslint/no-type-alias
export type EvaluatorSearch = z.infer<typeof evaluatorSearchSchema>
