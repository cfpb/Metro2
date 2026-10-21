import { Checkbox } from '@cfpb/design-system-react'
import Accordion from '@src/components/Accordion/Accordion'
import CheckboxFilterItem from '@src/pages/Evaluator/filters/components/CheckboxFilterItem'
import type { EvaluatorFacets } from '@src/types/EvaluatorFacets'
import { formatNumber } from '@src/utils/formatNumbers'
import { useNavigate } from '@tanstack/react-router'
import type { ReactElement } from 'react'

import { FILTER_VALUES } from '@src/constants/annotationLookups'

interface CheckboxGroupProperties {
  field: keyof typeof FILTER_VALUES
  groupName: string
  groupItems: (typeof FILTER_VALUES)[keyof typeof FILTER_VALUES][]
  validValues: (typeof FILTER_VALUES)[keyof typeof FILTER_VALUES][]
  selectedValues: (typeof FILTER_VALUES)[keyof typeof FILTER_VALUES][]
  counts?: EvaluatorFacets[keyof EvaluatorFacets]
  filteredCounts?: EvaluatorFacets[keyof EvaluatorFacets]
}

export default function CheckboxFilterGroup({
  field,
  groupName,
  groupItems,
  counts = {},
  // all the values in the data from this group
  validValues,
  // all the currently selected values (that are valid) for this group's parent field
  selectedValues,
  filteredCounts = {}
}: CheckboxGroupProperties): ReactElement {
  const navigate = useNavigate()

  const allSelected = validValues.every(item => selectedValues.includes(item))

  const someSelected = validValues.some(item => selectedValues.includes(item))

  const filteredValidValues = validValues.filter(val => val in filteredCounts)

  let groupCount = 0
  for (const val of filteredValidValues) {
    groupCount += filteredCounts[val] ?? 0
  }

  const onChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const { checked } = event.currentTarget
    const vals = checked
      ? [...selectedValues, ...validValues]
      : selectedValues.filter(value => !groupItems.includes(value))

    void navigate({
      resetScroll: false,
      to: '.',
      search: (previous: Record<string, unknown>) => {
        const parameters = { ...previous }
        if (vals.length > 0) {
          parameters[field] = [...new Set(vals)].toSorted()
        } else {
          delete parameters[field]
        }
        // reset page to 1
        parameters.page = 1
        parameters.show_counts = true
        return parameters
      }
    })
  }

  return (
    <>
      {validValues.length > 0 ? (
        <Accordion
          className='nested nested--level-2'
          hasBackground={false}
          openOnLoad={allSelected || someSelected}
          header={
            <Checkbox
              id={`${field}_${groupName}`}
              label={
                <div className='label-with-count'>
                  <span>{groupName}</span>
                  <span className='count'>
                    {groupCount > 0 ? formatNumber(groupCount) : ''}
                  </span>
                </div>
              }
              checked={allSelected}
              isIndeterminate={!allSelected && someSelected}
              onChange={onChange}
            />
          }>
          <>
            {groupItems.map(item => (
              <CheckboxFilterItem
                item={item}
                key={`${field}_${item}`}
                field={field}
                count={counts[item as keyof EvaluatorFacets[keyof EvaluatorFacets]]}
                filteredCount={
                  filteredCounts[
                    item as keyof EvaluatorFacets[keyof EvaluatorFacets]
                  ]
                }
                selected={selectedValues}
              />
            ))}
          </>
        </Accordion>
      ) : (
        <Accordion
          className='nested nested--level-2'
          hasBackground={false}
          key={groupName}
          disabled={true}
          header={<Checkbox id={groupName} label={groupName} disabled={true} />}>
          {null}
        </Accordion>
      )}
    </>
  )
}
