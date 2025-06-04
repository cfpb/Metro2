import { useNavigate, useSearch } from '@tanstack/react-router'
import { Icon, Link, LinkText } from 'design-system-react'
import type { MouseEvent, ReactElement } from 'react'

export default function EvaluatorResultsToggle(): ReactElement {
  const view: unknown = useSearch({
    strict: false,
    select: search => search.view
  })
  const navigate = useNavigate()

  const onClick = (event: MouseEvent<HTMLButtonElement>): void => {
    void navigate({
      resetScroll: false,
      to: '.',
      search: prev =>
        event.currentTarget.id === 'all-tab'
          ? { ...prev, view: 'all' }
          : { view: 'sample' }
    })
  }

  return (
    <div className='tabbed_navigation'>
      <div className='row row__content'>
        <fieldset className='o-form_fieldset' data-testid='results-view-toggle'>
          <button
            type='button'
            id='all-tab'
            onClick={onClick}
            className={`tab ${view === 'all' ? 'active' : ''}`}>
            <Icon name='filter' />
            <span className='link-text'>All results</span>
          </button>
          <button
            type='button'
            id='sample-tab'
            onClick={onClick}
            className={`tab ${view === 'sample' ? 'active' : ''}`}>
            <Icon name='search' />
            <span className='link-text'>Sample</span>
          </button>
          <Link href='../../../guide/table' className='table_guide'>
            <LinkText>
              See advanced table features
           </LinkText>
          </Link>
        </fieldset>
      </div>

    </div>
  )
}