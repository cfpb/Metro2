import DefinitionList from 'components/DefinitionList/DefinitionList'
import { Expandable, ExpandableGroup } from 'design-system-react'
import type User from 'models/User'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import { formatDate, formatLongDescription, formatNumber } from '../../utils/utils'
import type EvaluatorMetadata from './Evaluator'

interface EvaluatorSummaryProperties {
  metadata: EvaluatorMetadata
  user: User
  event: Event
}

const adminUrlPrefix = import.meta.env.DEV ? 'http://localhost:8000' : ''

const explanatoryFields = new Map([
  ['rationale', 'Rationale'],
  ['potential_harm', 'Potential harm'],
  ['crrg_reference', 'CRRG reference'],
  ['alternate_explanation', 'Alternate explanation']
])

// An evaluator's metadata contains four fields that are
// displayed in the 'How to evaluate these results' expandable.
// Most of the fields won't be populated at first, so we
// sort the fields into two lists, populated and empty, and
// display each set separately in the expandable.
const sortExplanatoryFields = (
  metadata: EvaluatorMetadata
): [string[], string[]] => {
  const populatedFields: string[] = []
  const emptyFields: string[] = []
  for (const [field] of explanatoryFields.entries()) {
    if (metadata[field as keyof EvaluatorMetadata]) {
      populatedFields.push(field)
    } else {
      emptyFields.push(field)
    }
  }
  return [populatedFields, emptyFields]
}

export default function EvaluatorSummary({
  metadata,
  user,
  event
}: EvaluatorSummaryProperties): ReactElement {
  const summaryItems = [
    {
      term: 'Data from',
      definition:
        event.date_range_start && event.date_range_end
          ? `${formatDate(event.date_range_start)} - ${formatDate(
              event.date_range_end
            )}`
          : ''
    },
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

  const [populatedFields, emptyFields] = sortExplanatoryFields(metadata)

  return (
    <div className='content-row summary-row'>
      <div className='content-l'>
        <div className='content-l_col content-l_col-1-3'>
          <h3 className='h2'>Details</h3>
          <DefinitionList items={summaryItems} />
        </div>
        <div className='content-l_col content-l_col-2-3'>
          <h3 className='h2'>Description</h3>
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
            </Expandable>
          </ExpandableGroup>
        </div>
      </div>
    </div>
  )
}
