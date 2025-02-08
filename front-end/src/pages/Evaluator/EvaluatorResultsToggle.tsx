import { useNavigate, useSearch } from '@tanstack/react-router'
import { RadioButton } from 'design-system-react'
import type { ReactElement } from 'react'

export default function EvaluatorResultsToggle(): ReactElement {
  const view: unknown = useSearch({
    strict: false,
    select: search => search.view
  })
  const navigate = useNavigate()

  const onChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
    void navigate({
      resetScroll: false,
      to: '.',
      search: prev => ({ ...prev, view: e.target.value as 'all' | 'sample' })
    })
  }

  return (
    <div className='row row__content'>
      <fieldset className='o-form_fieldset' data-testid='results-view-toggle'>
        <legend className='h4'>Show</legend>
        <RadioButton
          id='sample'
          name='evaluator-results-toggle'
          label='Representative sample'
          labelClassName=''
          labelInline
          checked={view !== 'all'}
          onChange={onChange}
          value='sample'
          data-testid='sample-results-button'
        />
        <RadioButton
          id='all'
          name='evaluator-results-toggle'
          label='All results'
          labelClassName=''
          labelInline
          checked={view === 'all'}
          onChange={onChange}
          value='all'
          data-testid='all-results-button'
        />
      </fieldset>
    </div>
  )
}
