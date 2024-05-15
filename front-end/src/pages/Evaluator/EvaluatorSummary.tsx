import DefinitionList from 'components/DefinitionList/DefinitionList'
import { Expandable, ExpandableGroup } from 'design-system-react'
import type { ReactElement } from 'react'
import { formatDate, formatLongDescription, formatNumber } from '../../utils/utils'
import type EvaluatorMetadata from './Evaluator'

interface EvaluatorSummaryProperties {
  metadata: EvaluatorMetadata
}

export default function EvaluatorSummary({
  metadata
}: EvaluatorSummaryProperties): ReactElement {
  const summaryItems = [
    // { term: 'Data from', definition: '' },
    {
      term: 'Duration of inconsistency',
      definition:
        metadata.inconsistency_start && metadata.inconsistency_end
          ? `${formatDate(metadata.inconsistency_start)} - ${formatDate(
              metadata.inconsistency_end
            )}`
          : ''
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
      term: 'Categories',
      definition: metadata.category ? metadata.category.join(', ') : null
    }
  ]

  return (
    <div className='content-row summary-row'>
      <div className='content-l'>
        <div className='content-l_col content-l_col-1-3'>
          <h2>Details</h2>
          <DefinitionList items={summaryItems} />
        </div>
        <div className='content-l_col content-l_col-2-3'>
          <h2>Description</h2>
          <p>{metadata.description}</p>
          <ExpandableGroup accordion groupId='AccordionGroup'>
            <Expandable header='Criteria evaluated'>
              <div
                className='long-description'
                dangerouslySetInnerHTML={{
                  __html: formatLongDescription(metadata.long_description)
                }}
              />
            </Expandable>
            <Expandable header='How to evaluate these results'>
              <p />
            </Expandable>
          </ExpandableGroup>
        </div>
      </div>
    </div>
  )
}
