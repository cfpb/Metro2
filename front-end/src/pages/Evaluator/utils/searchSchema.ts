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
export const minMaxValidator = fallback(
  z.union([z.number(), z.enum([''])]).optional(),
  ''
)

export const BooleanStringValidator = z
  .union([
    z.boolean().transform(val => val.toString()),
    z.enum(['any', 'true', 'false'])
  ])
  .optional()

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

export const listValueValidator = (
  field: keyof typeof M2_FIELD_LOOKUPS
): z.ZodOptional<z.ZodEffects<z.ZodAny, string[], unknown>> =>
  z
    .any()
    .transform(val => validateFieldValues(val, field))
    .optional()

export const evaluatorSchema = z.object({
  view: fallback(z.enum(['all', 'sample']), 'sample'),
  page: fallback(z.number().gt(0), 1),
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

// List of filters that can be applied to evaluator results
export const filterableFields = evaluatorSchema
  .keyof()
  .options.filter(key => !['page', 'view', 'page_size'].includes(key))

// eslint-disable-next-line @typescript-eslint/no-type-alias
export type EvaluatorSearch = z.infer<typeof evaluatorSearchSchema>
