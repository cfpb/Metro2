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

export const getFieldsToDisplay = (
  fields_used: string[],
  fields_display: string[]
): string[] => {
  // Create list by combining fields_used and fields_display, each sorted alphabetically,
  // with constant values consumer account number and activity date added at beginning
  const fields = [
    'cons_acct_num',
    'activity_date',
    ...fields_used.sort(),
    ...fields_display.sort()
  ]
  // If php is present, add php1 right after it so they'll be adjacent columns.
  // php1 does not appear in fields metadata lists
  // & the values are not in the data returned by the API --
  // they are generated on the front end when hits data is fetched
  const phpIndex = fields.indexOf('php')
  if (phpIndex > -1) fields.splice(phpIndex + 1, 0, 'php1')

  return fields
}

export const evaluatorSearchSchema = z
  .object({
    view: fallback(z.enum(['all', 'sample']), 'sample').default('sample'),
    page: fallback(z.number().gt(0), 1).default(1)
  })
  .transform((params): object =>
    params.view === 'sample' ? { ...params, page: 1 } : { ...params }
  )
