import CheckboxFilterSection from '@src/pages/Evaluator/filters/components/Checkbox/CheckboxFilterSection'
import type { EvaluatorFacets } from '@src/types/EvaluatorFacets'
import { useSearch } from '@tanstack/react-router'
import { type ReactElement } from 'react'

import { FILTER_VALUES } from '@src/constants/annotationLookups'

interface CheckboxFieldFilterProperties {
  field: keyof typeof FILTER_VALUES
  countsForThisField?: EvaluatorFacets[keyof EvaluatorFacets]
  filteredCountsForThisField?: EvaluatorFacets[keyof EvaluatorFacets]
  showCounts: boolean
}

export default function CheckboxFieldFilter({
  field,
  countsForThisField = {},
  filteredCountsForThisField = {},
  showCounts = false
}: CheckboxFieldFilterProperties): ReactElement {
  /**
  Get any currently applied filters for this field from the querystring
  */
  const currentFilterValues = useSearch({
    strict: false,
    select: search => {
      const searchField = search[field]
      return Array.isArray(searchField) ? searchField : []
    }
  })

  return (
    <CheckboxFilterSection
      showCounts={showCounts}
      field={field}
      counts={countsForThisField}
      filteredCounts={filteredCountsForThisField}
      isRequired={field === 'acct_stat'} // account status can't be blank
      selectedFilterValues={
        currentFilterValues as (typeof FILTER_VALUES)[keyof typeof FILTER_VALUES][]
      }
    />
  )
}
