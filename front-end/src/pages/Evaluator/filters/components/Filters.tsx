import { FILTER_VALUES } from '@src/constants/annotationLookups'
import CheckboxFilter from '@src/pages/Evaluator/filters/components/CheckboxFilter'
import EvaluatorCheckboxGroup from '@src/pages/Evaluator/filters/components/EvaluatorCheckboxGroup'
import type { EvaluatorFacets } from '@src/types/EvaluatorFacets'
import type { ReactElement } from 'react'
import EvaluatorBooleanFilter from './BooleanFilter'
import type { currencyRangeField } from './RangeFilter'
import EvaluatorRangeFilter from './RangeFilter'

interface EvaluatorFiltersData {
  counts?: EvaluatorFacets
  filteredCounts?: EvaluatorFacets
  showCounts?: boolean
}

// export const checkboxFilters = [
//   'acct_stat',
//   'compl_cond_cd',
//   'php1',
//   'pmt_rating',
//   'spc_com_cd',
//   'terms_freq',
//   'cons_info_ind',
//   'l1__change_ind'
// ] as const satisfies readonly (keyof EvaluatorFacets)[]

export const checkboxFilters = Object.keys(
  FILTER_VALUES
) as (keyof typeof FILTER_VALUES)[]

export default function Filters({
  counts = {},
  filteredCounts = {},
  showCounts = false
}: EvaluatorFiltersData): ReactElement {
  return (
    <div className='sidebar-background'>
      <fieldset
        className='o-form__fieldset filter-sidebar'
        data-testid='evaluator-filter-sidebar'>
        <div className='block block--sub block--flush-top'>
          <h2 className='h3'>Account details</h2>
          <p>
            Filters are under development. Some options may not be relevant for this
            evaluator.
          </p>
          {showCounts ? (
            <>
              {checkboxFilters.map(field => {
                return (
                  <CheckboxFilter
                    key={field}
                    field={field}
                    countsForThisField={counts[field]}
                    filteredCountsForThisField={filteredCounts[field]}
                  />
                )
              })}
            </>
          ) : (
            <>
              {checkboxFilters.map(field => {
                return <EvaluatorCheckboxGroup field={field} key={field} />
              })}
            </>
          )}
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
