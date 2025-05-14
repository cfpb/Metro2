import { useNavigate, useSearch, Link } from '@tanstack/react-router'
// import { RadioButton } from 'design-system-react'
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
    <div className='tabbed_navigation'>
      <div className='row row__content'>
        <fieldset className='o-form_fieldset' data-testid='results-view-toggle'>
        <Link
          // resetScroll={false}
          resetScroll={false}
          to='.'
          search={prev => ({ ...prev, view: 'all' })}
          className='tab'
          >
          All results
        </Link>
         
        <Link
          resetScroll={false}
          to='.'
          search={prev => ({ ...prev, view: 'sample' })}
          className='tab'
      
          // classes from CCDB / Complaint Explorer, set active class if activeTab prop === 'sample'
          // aria attributes from CCDB / Complaint Explorer
          >
          Sample
        </Link>
        </fieldset>
      </div>
    </div>
  )
}
