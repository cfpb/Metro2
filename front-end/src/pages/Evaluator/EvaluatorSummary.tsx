import Accordion from 'components/Accordion/Accordion'
import DefinitionList from 'components/DefinitionList/DefinitionList'
import type User from 'models/User'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import {
  formatDateRange,
  formatLongDescription,
  formatNumber
} from '../../utils/formatters'
import type EvaluatorMetadata from './Evaluator'
import { explanatoryFields, sortExplanatoryFields } from './EvaluatorUtils'

interface EvaluatorSummaryProperties {
  metadata: EvaluatorMetadata
  user: User
  event: Event
}

const adminUrlPrefix = import.meta.env.DEV ? 'http://localhost:8000' : ''

export default function EvaluatorSummary({
  metadata,
  user,
  event
}: EvaluatorSummaryProperties): ReactElement {
  const summaryItems = [
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
      term: 'Categories',
      definition: metadata.category ? metadata.category.join(', ') : null
    }
  ]

  const [populatedFields, emptyFields] = sortExplanatoryFields(metadata)

  return (
    <div className='row row__content row__summary' data-testid='evaluator-summary'>
      <div className='content-l'>
        <div className='content-l_col content-l_col-1-3'>
          <h3 className='h2'>Details</h3>
          <DefinitionList items={summaryItems} />
        </div>
        <div className='content-l_col content-l_col-2-3'>
          <h3 className='h2'>Description</h3>
          <p>{metadata.description}</p>
          <Accordion header='Criteria evaluated'>
            <div
              className='long-description'
              dangerouslySetInnerHTML={{
                __html: formatLongDescription(metadata.long_description)
              }}
            />
          </Accordion>

          <Accordion header='How to evaluate these results'>
            {populatedFields.length > 0
              ? populatedFields.map(field => (
                  <div key={field} className='u-mb15'>
                    <b>{explanatoryFields.get(field)}: </b>
                    <span>{metadata[field as keyof typeof metadata]}</span>
                  </div>
                ))
              : ''}
            {emptyFields.length > 0 ? (
              <div className='u-mb15'>
                <p>
                  <b>Help make this tool more useful:</b> Your experience and
                  knowledge about specific evaluators can help others.
                  {user.is_admin ? (
                    <span>
                      {' '}
                      As a Metro2 admin, you can{' '}
                      <a
                        href={`${adminUrlPrefix}/admin/evaluate_m2/evaluatormetadata/${metadata.id}/change/`}
                        target='_blank'
                        rel='noreferrer'>
                        add information directly to this evaluator.
                      </a>
                    </span>
                  ) : (
                    <span />
                  )}{' '}
                  Consider adding:
                </p>
                <ul>
                  {emptyFields.map(field => (
                    <li key={field}>{explanatoryFields.get(field)}</li>
                  ))}
                </ul>
              </div>
            ) : (
              ''
            )}
          </Accordion>
        </div>
      </div>
    </div>
  )
}
