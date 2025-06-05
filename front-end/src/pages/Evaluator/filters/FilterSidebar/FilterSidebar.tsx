import type { ReactElement } from 'react'
import type { EvaluatorSearch } from '../../utils/searchSchema'
import EvaluatorBooleanFilter from '../BooleanFilter'
import EvaluatorCheckboxGroup from '../CheckboxGroup'
import EvaluatorRangeFilter from '../RangeFilter'
import './FilterSidebar.less'

export default function EvaluatorFilterSidebar(): ReactElement {
  return (
    <fieldset
      className='o-form_fieldset filter-sidebar'
      data-testid='evaluator-filter-sidebar'>
      <div className='block block__sub block__flush-top'>
        <h2 className='h3'>Account details</h2>
        <p>
          Filters are under development. Some options may not be relevant for this
          evaluator.
        </p>
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
          <h2 className='h3'>Dates</h2>
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
          <h2 className='h3'>Amounts</h2>
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
