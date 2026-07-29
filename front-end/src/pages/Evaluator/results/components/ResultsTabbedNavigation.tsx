import { Tab, TabList } from '@cfpb/design-system-react'
import { useNavigate, useSearch } from '@tanstack/react-router'
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
          view: event.currentTarget.id === 'tab-all' ? 'all' : 'sample',
          page: 1,
          sort: 'activity_date'
        }
      }
    })
  }

  return (
    <TabList>
      <Tab
        id='all'
        iconLeft='filter'
        onClick={onClick}
        isActive={view === 'all'}
        data-testid='all-results-tab'>
        All results
      </Tab>
      <Tab
        id='search'
        iconLeft='search'
        onClick={onClick}
        isActive={view !== 'all'}
        data-testid='sample-results-tab'>
        Sample
      </Tab>
    </TabList>
  )
}
