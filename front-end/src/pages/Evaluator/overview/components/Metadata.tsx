import type EvaluatorMetadata from '@src/types/EvaluatorMetadata'
import type { ReactElement } from 'react'
export const adminUrlPrefix = import.meta.env.DEV ? 'http://localhost:8000' : ''

/**
 * EvaluatorMetadata
 *
 * An evaluator's metadata contains four fields that are displayed
 * in the 'How to evaluate these results' section of the evaluator page.
 *
 * Most of the fields won't have content at first, so we check for
 * populated fields and display any that exist.
 *
 * We also display information on how users can contribute content 
 * for the empty fields or update content for populated fields.
 *
 */

interface MetadataProps {
  metadata: EvaluatorMetadata
  isAdmin: boolean
}

export const explanatoryFields = new Map([
  ['rationale', 'Rationale'],
  ['potential_harm', 'Potential harm'],
  ['alternate_explanation','Alternate explanation'],
  ['crrg_reference','CRRG reference']
])

export const getPopulatedMetadataFields = (
  metadata: EvaluatorMetadata
): string[] => {
  const populatedFields: string[] = []
  for (const [field] of explanatoryFields.entries()) {
    if (metadata[field as keyof EvaluatorMetadata]) {
      populatedFields.push(field)
    } 
  }
  return populatedFields
}

export default function EvaluatorMetadataSection({
  metadata,
  isAdmin = false
}: MetadataProps): ReactElement {
  
  const populatedFields = getPopulatedMetadataFields(metadata)
  const hasMetadata = populatedFields.length > 0

  return (
    <div className='metadata-expandable-content'>
      {hasMetadata ? 
        <div data-testid='metadata-section' className='metadata-section u-mb30'>
          {populatedFields.map(field => (
            <>
              <h4>{explanatoryFields.get(field)}</h4>
              <div dangerouslySetInnerHTML={{ __html: metadata[field as keyof EvaluatorMetadata] ?? '' }}></div>
            </>
          ))}
        </div>
      : 
        <>
          <h4>Add additional context for this evaluator</h4>
          <p>Information contributed by users like you will help make the tool easier to understand and more useful for everyone.</p>
        </>
      }
      {isAdmin ? (
        <p data-testid='metadata-cta__admin'>
          {' '}
          As a Metro2 admin, you can{' '}
          <a
            href={`${adminUrlPrefix}/admin/evaluate_m2/evaluatormetadata/${metadata.id}/change/`}
            target='_blank'
            rel='noreferrer'>
            contribute additional context
          </a> directly to this evaluator.
        </p>
      ) : (
        <>
          {hasMetadata ? 
            <p>To contribute additional context for this evaluator, please contact a Metro2 admin.</p>
          : 
            <p className='u-mt15'><a href='/guide/contribute' target='_blank' rel='noreferrer'>See the user guide</a> for examples or contact a Metro 2 administrator to contribute additional context for this evaluator.</p>
          }
        </>      
      )}
    </div>
  )
}
