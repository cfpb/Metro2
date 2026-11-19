import FilterCounts from '@src/pages/Evaluator/filters/components/FilterCounts'
import type { ReactElement } from 'react'
import Filters from './components/Filters'
import './FilterSidebar.scss'

const hitsLimit = 1_000_000
const hitsCountMessage =
  'Filter counts are not available for evaluators with over a million results.'

interface EvaluatorSidebarData {
  evaluatorId: string
  eventId: string | number
  hits: number
}

export default function EvaluatorFilterSidebar({
  evaluatorId,
  eventId,
  hits = 0
}: EvaluatorSidebarData): ReactElement {
  const showFilterCounts = hits < hitsLimit

  return (
    <div className='results__sidebar sidebar'>
      {showFilterCounts ? (
        <FilterCounts eventId={eventId} evaluatorId={evaluatorId} />
      ) : (
        <Filters message={hits > hitsLimit ? hitsCountMessage : null} />
      )}
    </div>
  )
}
