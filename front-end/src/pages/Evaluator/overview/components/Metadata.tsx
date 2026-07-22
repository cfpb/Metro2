import Accordion from '@src/components/Accordion/Accordion'
import type EvaluatorMetadata from '@src/types/EvaluatorMetadata'
import { formatDate } from '@src/utils/formatDates'
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
  ['alternate_explanation', 'Alternate explanation'],
  ['crrg_reference', 'CRRG reference']
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
    <>
      <Accordion
        header='How to evaluate these results'
        className='evaluate-expandable'>
        <div className='metadata-expandable-content'>
          {hasMetadata ? (
            <div data-testid='metadata' className='metadata-section '>
              {populatedFields.map(field => (
                <>
                  <h4>{explanatoryFields.get(field)}</h4>
                  <div
                    data-testid={field}
                    dangerouslySetInnerHTML={{
                      __html: metadata[field as keyof EvaluatorMetadata] ?? ''
                    }}></div>
                </>
              ))}
            </div>
          ) : (
            <div data-testid='no-metadata-message' className='u-mb15'>
              <h4>Add additional context for this evaluator</h4>
              <p>
                Information contributed by users like you will help make the tool
                easier to understand and more useful for everyone.
              </p>
            </div>
          )}

          <div className='contribute-instructions'>
            {isAdmin === true ? (
              <p data-testid='metadata-contribute-admin'>
                {' '}
                As a Metro2 admin, you can{' '}
                <a
                  href={`${adminUrlPrefix}/admin/evaluate_m2/evaluatormetadata/${metadata.id}/change/`}
                  target='_blank'
                  rel='noreferrer'>
                  contribute additional context
                </a>{' '}
                directly to this evaluator.
              </p>
            ) : (
              <>
                {hasMetadata ? (
                  <p data-testid='metadata-contribute '>
                    To contribute additional context for this evaluator, please
                    contact a Metro2 admin.
                  </p>
                ) : (
                  <p data-testid='no-metadata-contribute'>
                    <a href='/guide/contribute' target='_blank' rel='noreferrer'>
                      See the user guide
                    </a>{' '}
                    for examples or contact a Metro 2 administrator to contribute
                    additional context for this evaluator.
                  </p>
                )}
              </>
            )}
          </div>
          {metadata.interpret_fields_last_modified ? (
            <p
              data-testid='interpret-fields-last-modified'
              className='last-modified-date'>
              This data was last modified{' '}
              <span data-testid='interpret-fields-last-modified-date'>
                {formatDate(metadata.interpret_fields_last_modified, 'fullText')}.
              </span>
            </p>
          ) : null}
        </div>
      </Accordion>
      {metadata.additional_notes ? (
        <Accordion header='Additional notes' className='additional-notes-expandable'>
          <div className='metadata-expandable-content'>
            <p
              data-testid='additional-notes'
              dangerouslySetInnerHTML={{
                __html: metadata.additional_notes
              }}
            />
            {metadata.additional_notes_last_modified ? (
              <p
                data-testid='additional-notes-last-modified'
                className='last-modified-date'>
                This data was last modified{' '}
                <span data-testid='additional-notes-last-modified-date'>
                  {formatDate(metadata.additional_notes_last_modified, 'fullText')}.
                </span>
              </p>
            ) : null}
          </div>
        </Accordion>
      ) : null}
    </>
  )
}
