import Accordion from 'components/Accordion/Accordion'
import type User from 'models/User'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import type EvaluatorMetadata from 'types/Evaluator'
import EvaluatorLongDescription from './LongDescription'
import EvaluatorMetadataSection from './Metadata'
import EvaluatorSummary from './Summary'

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
    <div className='row row__content row__summary' data-testid='evaluator-summary'>
      <div className='content-l'>
        <div className='content-l_col content-l_col-1-3'>
          <h3 className='h2'>Details</h3>
          <EvaluatorSummary event={event} metadata={metadata} />
        </div>
        <div className='content-l_col content-l_col-2-3'>
          <h3 className='h2'>Description</h3>
          <p className='evaluator-description'>{metadata.description}</p>
          <div className='evaluator-metadata'>
            <Accordion header='Criteria evaluated'>
              <div className='long-description'>
                <EvaluatorLongDescription content={metadata.long_description} />
              </div>
            </Accordion>
            <Accordion header='How to evaluate these results'>
              <EvaluatorMetadataSection
                isAdmin={user.is_admin}
                metadata={metadata}
              />
            </Accordion>
          </div>
        </div>
      </div>
    </div>
  )
}
