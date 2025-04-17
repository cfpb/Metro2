import type { ReactElement } from 'react'
import type { EvaluatorSearch } from '../utils/searchSchema'
import EvaluatorBooleanFilter from './BooleanFilter'
import EvaluatorCheckboxGroup from './CheckboxGroup'
import EvaluatorRangeFilter from './RangeFilter'

export default function EvaluatorFilterSidebar(): ReactElement {
  return (
    <fieldset className='o-form_fieldset' data-testid='evaluator-filter-sidebar'>
      <div className='block block__sub block__flush-top'>
        <p>
          Filters are under development. Some options may not be relevant for this
          evaluator.
        </p>
        <h2 className='h3'>Filter results by account details</h2>
        {[
          'acct_stat',
          'compl_cond_cd',
          'php1',
          'pmt_rating',
          'spc_com_cd',
          'terms_freq',
          'account_holder__cons_info_ind',
          'account_holder__cons_info_ind_assoc',
          'l1__change_ind'
        ].map(field => (
          <EvaluatorCheckboxGroup
            field={field as keyof EvaluatorSearch}
            key={field}
          />
        ))}
        <div className='block block__sub'>
          <h2 className='h3'>Filter by dates</h2>
          <EvaluatorBooleanFilter
            field={'dofd' as keyof EvaluatorSearch}
            header='Date of first delinquency (DOFD)'
            checkboxLabel='DOFD'
          />
          <EvaluatorBooleanFilter
            field={'date_closed' as keyof EvaluatorSearch}
            header='Date closed'
            checkboxLabel='date closed'
          />
        </div>
        <div className='block block__sub'>
          <h2 className='h3'>Filter by amounts</h2>
          {['amt_past_due', 'current_bal'].map(field => (
            <EvaluatorRangeFilter
              key={field}
              field={field as keyof EvaluatorSearch}
            />
          ))}
        </div>
      </div>
    </fieldset>
  )
}
