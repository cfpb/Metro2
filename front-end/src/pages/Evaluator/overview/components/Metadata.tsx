import type { ReactElement } from 'react'
import type EvaluatorMetadata from 'types/EvaluatorMetadata'

export const adminUrlPrefix = import.meta.env.DEV ? 'http://localhost:8000' : ''

/**
 * EvaluatorMetadata
 *
 * An evaluator's metadata contains four fields that are displayed
 * in the 'How to evaluate these results' section of the evaluator page.
 *
 * Most of the fields won't have content at first, so we separate the
 * fields into two arrays based on whether they're populated and display
 * the lists separately.
 *
 * If any of the fields are unpopulated, we also display information on
 * how users can contribute content for the empty fields.
 *
 */

interface MetadataProps {
  metadata: EvaluatorMetadata
  isAdmin: boolean
}

export const explanatoryFields = new Map([
  [
    'rationale',
    {
      title: 'Rationale',
      description:
        "Explains why the inconsistency found by this evaluator is a problem and describes what's required for the account to be accurately furnished."
    }
  ],
  [
    'potential_harm',
    {
      title: 'Potential harm',
      description:
        "Describes the negative impact this inconsistency might have on an individual's credit."
    }
  ],
  [
    'alternate_explanation',
    {
      title: 'Alternate explanation',
      description:
        'Describes any logical reasons for this inconsistency to exist when the account has been accurately furnished.'
    }
  ],
  [
    'crrg_reference',
    {
      title: 'CRRG reference',
      description:
        'Includes references to specific sections of the Credit Reporting Resource Guide (CRRG) that may be useful for interpreting the results of this evaluator.'
    }
  ]
])

/**
 * sortExplanatoryFields()
 *
 * Sorts metadata fields into two ordered arrays, one for fields that have a value
 * in this evaluator's metadata object and one for fields that do not have a value.
 *
 * @param {array} metadata - an object containing metadata about an evaluator
 * @returns {array} Returns an array containing two lists:
 *                    1. the explanatory fields that have values in the metadata
 *                    2. the explanatory fields that don't have values in the metadata
 * @example metadata = {rationale: '', potential_harm: 'Lorem ipsum', alternate_explanation: 'Lorem ipsum'}
 *          returns: [
 *                    ['potential_harm', 'alternate_explanation'], // populated fields
 *                    ['rationale', 'crrg_reference'] // empty fields
 *                   ]
 */

export const sortExplanatoryFields = (
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

export default function EvaluatorMetadataSection({
  metadata,
  isAdmin
}: MetadataProps): ReactElement {
  const [populatedFields, emptyFields] = sortExplanatoryFields(metadata)

  return (
    <div data-testid='metadata-section'>
      {populatedFields.length > 0 ? (
        <ul
          className='m-list m-list__unstyled'
          data-testid='metadata-populated-fields'>
          {populatedFields.map(field => (
            <li key={field} className='u-mb15'>
              <b>{explanatoryFields.get(field)?.title}: </b>
              <span>{metadata[field as keyof typeof metadata]}</span>
            </li>
          ))}
        </ul>
      ) : null}

      {emptyFields.length > 0 ? (
        <div className='block block__sub u-mb15' data-testid='metadata-contribute'>
          <p>
            <b>We still need metadata for this evaluator.</b> Metadata contributed by
            users like you will help make the tool easier to understand and more
            useful for everyone. This evaluator is missing:
          </p>
          <ul data-testid='metadata-empty-fields'>
            {emptyFields.map(field => {
              const fieldProps = explanatoryFields.get(field)
              return (
                <li key={field}>
                  <b>{fieldProps?.title}</b>: {fieldProps?.description}
                </li>
              )
            })}
          </ul>
          <p data-testid='metadata-cta'>
            <span data-testid='metadata-cta_general'>
              For examples and more information on how to contribute to this
              evaluator,{' '}
              <a href='/guide/contribute' target='_blank' rel='noreferrer'>
                follow these directions.
              </a>
            </span>
            {isAdmin ? (
              <span data-testid='metadata-cta_admin'>
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
          </p>
        </div>
      ) : null}
    </div>
  )
}
