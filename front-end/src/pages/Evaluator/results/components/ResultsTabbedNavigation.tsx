import { useNavigate, useSearch } from '@tanstack/react-router'
import TabbedNavigation from 'components/TabbedNavigation/TabbedNavigation'
import type { ReactElement } from 'react'

export default function EvaluatorResultsTabbedNavigation(): ReactElement {
  const view: string | undefined = useSearch({
    strict: false,
    select: search => search.view
  })
  const navigate = useNavigate()

  const onClick = (event: React.MouseEvent<HTMLButtonElement>): void => {
    void navigate({
      resetScroll: false,
      to: '.',
      search: (): object => {
        return {
          view: event.currentTarget.id === 'all-results-tab' ? 'all' : 'sample',
          page: 1,
          sort: 'activity_date'
        }
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
