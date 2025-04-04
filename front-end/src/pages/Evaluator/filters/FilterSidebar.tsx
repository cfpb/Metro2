import type { ReactElement } from 'react'
import type { EvaluatorSearch } from '../utils/searchSchema'
import EvaluatorRangeFilter from './RangeFilter'

export default function EvaluatorFilterSidebar(): ReactElement {
  return (
    <fieldset className='o-form_fieldset'>
      <div className='block block__sub block__flush-top'>
        <h2 className='h3'>Filter by amounts</h2>
        {['amt_past_due', 'current_bal'].map(field => (
          <EvaluatorRangeFilter key={field} field={field as keyof EvaluatorSearch} />
        ))}
      </div>
    </fieldset>
  )
}
