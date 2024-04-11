import DefinitionList from 'components/DefinitionList/DefinitionList'
import type { ReactElement } from 'react'
import { formatNumber } from 'utils/utils'
import type EvaluatorMetadata from './Evaluator'

interface EvaluatorSummaryProperties {
  metadata: EvaluatorMetadata
}

export default function EvaluatorSummary({
  metadata
}: EvaluatorSummaryProperties): ReactElement {
  const summaryItems = [
    { term: 'Duration', definition: '' },
    {
      term: 'Total inconsistencies',
      // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
      definition: formatNumber(metadata.hits)
    },
    {
      term: 'Total accounts affected',
      // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
      definition: formatNumber(metadata.accounts)
    },
    { term: 'Category', definition: metadata.category }
  ]

  return (
    <div className='content-row u-mt30'>
      <div className='content-l'>
        <div className='content-l_col content-l_col-1-3'>
          <h3>Details</h3>
          <DefinitionList items={summaryItems} />
        </div>
        <div className='content-l_col content-l_col-1-3'>
          <h3>Description</h3>
          <p>{metadata.description}</p>
          {/* <div dangerouslySetInnerHTML={{ __html: metadata.long_description }} /> */}
        </div>
      </div>
    </div>
  )
}
