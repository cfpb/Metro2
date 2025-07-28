import TabbedNavigation from '@src/components/TabbedNavigation/TabbedNavigation'
import { useNavigate, useSearch } from '@tanstack/react-router'
import type { ReactElement } from 'react'

export default function EvaluatorResultsTabs(): ReactElement {
  const view: unknown = useSearch({
    strict: false,
    select: search => search.view
  })
  const navigate = useNavigate()

  const onClick = (event: React.MouseEvent<HTMLButtonElement>): void => {
    void navigate({
      resetScroll: false,
      to: '.',
      search: prev =>
        event.currentTarget.id === 'all-results-tab'
          ? { ...prev, view: 'all' }
          : { view: 'sample' }
    })
  }

  return (
    <TabbedNavigation
      onClick={onClick}
      tabs={[
        {
          id: 'all-results-tab',
          isActive: view === 'all',
          icon: 'filter',
          text: 'All results'
        },
        {
          id: 'sample-results-tab',
          isActive: view !== 'all',
          icon: 'search',
          text: 'Sample'
        }
      ]}
    />
  )
}
