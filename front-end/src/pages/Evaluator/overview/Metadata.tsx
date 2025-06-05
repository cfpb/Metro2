import type { ReactElement } from 'react'
import type EvaluatorMetadata from 'types/Evaluator'
import { adminUrlPrefix } from '../utils/constants'

interface MetadataProps {
  metadata: EvaluatorMetadata
  isAdmin: boolean
}

export const explanatoryFields = new Map([
  ['rationale', 'Rationale'],
  ['potential_harm', 'Potential harm'],
  ['crrg_reference', 'CRRG reference'],
  ['alternate_explanation', 'Alternate explanation']
])

/**
 * sortExplanatoryFields()
 *
 * An evaluator's metadata contains four fields that are displayed
 * in the 'How to evaluate these results' section of the evaluator page.
 * Most of the fields won't have content at first, so we separate the
 * fields into two arrays based on whether they're populated and display
 * the lists separately.
 *
 * @param {array} metadata - an object containing metadata about an evaluator
 * @returns {array} Returns an array containing two lists:
 *                    1. the explanatory fields that have values in the metadata
 *                    2. the explanatory fields that don't have values in the metadata
 * @example metadata = {rationale: '', potential_harm: 'Lorem ipsum', alternate_explanation: 'Lorem ipsum'}
 *          returns: [
 *                    ['potential_harm', 'alternate_explanation'],
 *                    ['rationale', 'crrg_reference']
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
    <>
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
            <b>Help make this tool more useful:</b> Your experience and knowledge
            about specific evaluators can help others.
            {isAdmin ? (
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
    </>
  )
}
