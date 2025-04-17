import { useNavigate, useSearch } from '@tanstack/react-router'
import { RadioButton } from 'design-system-react'
import type { ReactElement } from 'react'

export default function EvaluatorResultsToggle(): ReactElement {
  const view: unknown = useSearch({
    strict: false,
    select: search => search.view
  })
  const navigate = useNavigate()

  const onChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    void navigate({
      resetScroll: false,
      to: '.',
      search: prev =>
        event.target.value === 'all' ? { ...prev, view: 'all' } : { view: 'sample' }
    })
  }

  return (
    <div className='row row__content block block__sub'>
      <fieldset className='o-form_fieldset' data-testid='results-view-toggle'>
        <legend className='h4'>Options</legend>
        <RadioButton
          id='sample'
          name='evaluator-results-toggle'
          label='View representative sample'
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
          label='View and filter all results'
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
