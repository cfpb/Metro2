import TabbedNavigation from '@src/components/TabbedNavigation/TabbedNavigation'
import { useNavigate, useSearch } from '@tanstack/react-router'
import type { ReactElement } from 'react'

export default function EvaluatorResultsTabbedNavigation(): ReactElement {
  const view: unknown = useSearch({
    strict: false,
    select: search => search.view
  })
  const navigate = useNavigate()

  const onClick = (event: React.MouseEvent<HTMLButtonElement>): void => {
    void navigate({
      resetScroll: false,
      to: '.',
      search: prev => {
        if (event.currentTarget.id === 'all-results-tab') {
          return { ...prev, view: 'all', page: 1 }
        }
        return prev.sort
          ? // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-return
            { sort: prev.sort, view: 'sample', page: 1 }
          : { view: 'sample', page: 1 }
      }
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
