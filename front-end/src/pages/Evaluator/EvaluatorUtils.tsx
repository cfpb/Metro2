import { fallback } from '@tanstack/router-zod-adapter'
import { z } from 'zod'
import type EvaluatorMetadata from './Evaluator'

export const ITEMS_PER_PAGE = 20

export const explanatoryFields = new Map([
  ['rationale', 'Rationale'],
  ['potential_harm', 'Potential harm'],
  ['crrg_reference', 'CRRG reference'],
  ['alternate_explanation', 'Alternate explanation']
])

// An evaluator's metadata contains four fields that are
// displayed in the 'How to evaluate these results' expandable.
// Most of the fields won't be populated at first, so we
// sort the fields into two lists, populated and empty, and
// display the two sets separately.
export const sortExplanatoryFields = (
  metadata: EvaluatorMetadata
): [string[], string[]] => {
  const populatedFields: string[] = []
  const emptyFields: string[] = []
  for (const [field] of explanatoryFields.entries()) {
    if (metadata[field as keyof EvaluatorMetadata]) {
      populatedFields.push(field)
    } else {
      emptyFields.push(field)
    }
  }
  return [populatedFields, emptyFields]
}

export const getPageCount = (resultsCount: number): number =>
  Math.ceil(resultsCount / ITEMS_PER_PAGE)

export const getResultsMessage = (
  resultsCount: number,
  itemCount: number,
  view: 'all' | 'sample' | undefined = 'sample',
  page: number | undefined = 1
): string => {
  if (view === 'all') {
    const start = (page - 1) * ITEMS_PER_PAGE + 1
    const end =
      page * ITEMS_PER_PAGE > resultsCount ? resultsCount : page * ITEMS_PER_PAGE
    return `Showing ${start}-${end} of ${resultsCount} results`
  }
  return `Showing ${
    resultsCount > 20 ? 'representative sample of' : ''
  } ${itemCount} out of ${resultsCount} results`
}

/**
 * getTableFields()
 *
 * Generate list of fields that will appear as columns in the table for this evaluator's
 * results.
 *
 * The results table for each evaluator shows a custom subset of M2 fields that are useful
 * for understanding the scenario the specific evaluator is targeting.
 *
 * The list of fields displayed in the table is created by combining two lists from the evaluator's metadata
 * (fields_used--fields that are actually checked by the evaluator, & fields_display--other helpful fields)
 * with some default fields that are shown for each evaluator.
 *
 * We also check to see whether PHP is one of the fields for display in this table
 * and, if so, add a PHP1 column next to PHP. (We use the first character of the 24 character
 * payment history profile field in evaluators, but php1 values are separated out
 * on the front end and not returned from the API.)
 *
 * TODO: PHP1 should be handled by the back end / API / appear in metadata fields_used lists
 * TODO: PHP / PHP1 will soon be one of the fields that's shown for all evaluators
 *       Will it be included in the metadata for each eval, or added here like 'activity_date'?
 *
 * @param {array} fields_used - list of fields used by this eval
 * @param {array} fields_display - list of fields that are also relevant to this eval
 * @returns {array} Returns a list of fields that will be columns in the results table
 */

export const getTableFields = (
  fields_used: string[],
  fields_display: string[]
): string[] => {
  const fields = [
    'cons_acct_num',
    'activity_date',
    ...fields_used.sort(),
    ...fields_display.sort()
  ]

  const phpIndex = fields.indexOf('php')
  if (phpIndex > -1) fields.splice(phpIndex + 1, 0, 'php1')

  return fields
}

export const evaluatorSearchSchema = z
  .object({
    view: fallback(z.enum(['all', 'sample']), 'sample').default('sample'),
    page: fallback(z.number().gt(0), 1).default(1),
    amt_past_due_min: z.number().optional(),
    amt_past_due_max: z.number().optional(),
    current_bal_min: z.number().optional(),
    current_bal_max: z.number().optional()
  })
  .transform((params): object =>
    params.view === 'sample' ? { ...params, page: 1 } : { ...params }
  )

// eslint-disable-next-line @typescript-eslint/no-type-alias
export type EvaluatorSearch = z.infer<typeof evaluatorSearchSchema>
