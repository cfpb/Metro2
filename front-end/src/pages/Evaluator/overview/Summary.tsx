import type { Definition } from 'components/DefinitionList/DefinitionList'
import DefinitionList from 'components/DefinitionList/DefinitionList'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import type EvaluatorMetadata from 'types/Evaluator'
import { formatDateRange, formatNumber } from 'utils/formatters'

interface EvaluatorSummaryProperties {
  metadata: EvaluatorMetadata
  event: Event
}

export default function EvaluatorSummary({
  metadata,
  event
}: EvaluatorSummaryProperties): ReactElement {
  return (
    <DefinitionList
      items={
        [
          {
            term: 'Data from',
            definition: formatDateRange(event.date_range_start, event.date_range_end)
          },
          {
            term: 'Duration of inconsistency',
            definition: formatDateRange(
              metadata.inconsistency_start,
              metadata.inconsistency_end
            )
          },
          {
            term: 'Total inconsistencies',
            definition: formatNumber(metadata.hits)
          },
          {
            term: 'Total accounts affected',
            definition: formatNumber(metadata.accounts_affected)
          },
          {
            term: 'Category',
            definition: metadata.category
          }
        ] as Definition[]
      }
    />
  )
}
