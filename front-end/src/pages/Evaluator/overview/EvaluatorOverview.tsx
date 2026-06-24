import DOMPurify from 'dompurify'
import Accordion from '@src/components/Accordion/Accordion'
import type EvaluatorMetadata from '@src/types/EvaluatorMetadata'
import type Event from '@src/types/Event'
import type User from '@src/types/User'
import type { ReactElement } from 'react'
import EvaluatorMetadataSection from './components/Metadata'
import EvaluatorSummary from './components/Summary'

import './EvaluatorOverview.scss'

interface EvaluatorOverviewProperties {
  metadata: EvaluatorMetadata
  user: User
  event: Event
}

export default function EvaluatorOverview({
  metadata,
  user,
  event
}: EvaluatorOverviewProperties): ReactElement {
  return (
    <div className='row row--content row--summary' data-testid='evaluator-summary'>
      <div className='content-l'>
        <div className='content-l__col content-l__col-1-3'>
          <h2>Details</h2>
          <EvaluatorSummary event={event} metadata={metadata} />
        </div>
        <div className='content-l__col content-l__col-2-3'>
          <h2>Description</h2>
          <p className='evaluator-description '>{metadata.description}</p>
          <div className='evaluator-metadata'>
            <Accordion header='Criteria evaluated'>
              <div className='long-description'>
                <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(metadata.long_description) }}>
          </div>
              </div>
            </Accordion>
            <Accordion header='How to evaluate these results'>
              <EvaluatorMetadataSection
                metadata={metadata}
                isAdmin={user.is_admin}
              />
            </Accordion>
          </div>
        </div>
      </div>
    </div>
  )
}
