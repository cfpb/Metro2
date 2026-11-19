import { FILTER_VALUES } from '@src/constants/annotationLookups'
import CheckboxFilter from '@src/pages/Evaluator/filters/components/Checkbox/CheckboxFilter'
import type { EvaluatorFacets } from '@src/types/EvaluatorFacets'
import type { ReactElement } from 'react'
import EvaluatorBooleanFilter from './BooleanFilter'
import type { currencyRangeField } from './RangeFilter'
import EvaluatorRangeFilter from './RangeFilter'

interface EvaluatorFiltersData {
  counts?: EvaluatorFacets
  filteredCounts?: EvaluatorFacets
  showCounts?: boolean
  message?: string | null
}

export const checkboxFilters = Object.keys(
  FILTER_VALUES
) as (keyof typeof FILTER_VALUES)[]

export default function Filters({
  counts = {},
  filteredCounts = {},
  showCounts = false,
  message
}: EvaluatorFiltersData): ReactElement {
  return (
    <div className='sidebar-background'>
      <fieldset
        className='o-form__fieldset filter-sidebar'
        data-testid='evaluator-filter-container'>
        <div className='block block--sub block--flush-top'>
          <h2 className='h3'>Account details</h2>
          <>
            {message ? <p data-testid='counts-message'>{message}</p> : null}
            {checkboxFilters.map(field => {
              return (
                <CheckboxFilter
                  key={field}
                  field={field}
                  showCounts={showCounts}
                  countsForThisField={counts[field]}
                  filteredCountsForThisField={filteredCounts[field]}
                />
              )
            })}
          </>
          <div className='block block--sub'>
            <h2 className='h3'>Dates</h2>
            <EvaluatorBooleanFilter
              field='dofd'
              header='Date of first delinquency (DOFD)'
              checkboxLabel='DOFD'
            />
            <EvaluatorBooleanFilter
              field='date_closed'
              header='Date closed'
              checkboxLabel='date closed'
            />
          </div>
          <div className='block block--sub'>
            <h2 className='h3'>Amounts</h2>
            {['amt_past_due', 'current_bal'].map(field => (
              <EvaluatorRangeFilter
                key={field}
                field={field as currencyRangeField}
              />
            ))}
          </div>
        </div>
      </fieldset>
    </div>
  )
}
