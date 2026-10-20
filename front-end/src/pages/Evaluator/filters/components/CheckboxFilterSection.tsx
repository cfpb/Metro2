import { useNavigate } from '@tanstack/react-router'
import type { ReactElement } from 'react'

import { Checkbox } from '@cfpb/design-system-react'
import Accordion from '@src/components/Accordion/Accordion'
import { FILTER_VALUES } from '@src/constants/annotationLookups'
import fieldGroups from '@src/constants/filterFieldGroups'
import CheckboxFilterGroup from '@src/pages/Evaluator/filters/components/CheckboxFilterGroup'
import CheckboxFilterItem from '@src/pages/Evaluator/filters/components/CheckboxFilterItem'
import type { EvaluatorFacets } from '@src/types/EvaluatorFacets'
import getHeaderName from '@src/utils/getHeaderName'

interface CheckboxFieldFilterProperties {
  // name of the M2 field this filter is for
  field: keyof typeof FILTER_VALUES
  // all the values for this field that are selected in the querystring
  selectedFilterValues?: (typeof FILTER_VALUES)[keyof typeof FILTER_VALUES][]
  // an object that includes counts for initial valid values (values that appear in the unfiltered data)
  counts?: EvaluatorFacets[keyof EvaluatorFacets]
  // an object that includes counts for filtered valid values (values that appear in the filtered data)
  filteredCounts?: EvaluatorFacets[keyof EvaluatorFacets]
  // whether the field is required
  isRequired?: boolean
}

const CheckboxFilterSection = function CheckboxFilterParent({
  field,
  selectedFilterValues = [],
  counts = {},
  filteredCounts = {},
  isRequired = false
}: CheckboxFieldFilterProperties): ReactElement {
  const navigate = useNavigate()

  const onChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const { checked } = event.currentTarget
    const vals = checked ? Object.keys(counts) : []
    void navigate({
      resetScroll: false,
      to: '.',
      search: (previous: Record<string, unknown>) => {
        const parameters = { ...previous }
        if (vals.length > 0) {
          parameters[field] = vals.toSorted()
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

  // Get display name for field
  const fieldName = getHeaderName(field)

  // If the only initial value for this filter is 'blank',
  // the expandable should show as inactive
  if (Object.keys(counts).every(value => value === 'blank')) {
    return (
      <Accordion
        className='nested nested--level-1'
        disabled={true}
        hasBackground={false}
        header={
          <Checkbox id={field} label={fieldName} disabled={true} />
        }></Accordion>
    )
  }

  const hasGroups = field in fieldGroups

  // The values for this field that are initially valid / present in the data
  // const validValues = Object.keys(counts) as CheckboxFilterValues[]
  const validValues = Object.keys(
    counts
  ) as (typeof FILTER_VALUES)[keyof typeof FILTER_VALUES][]

  // Filter the currently selected values to make sure they're valid
  // This way if the URL is edited so that acct_stat=71,73, but only 71 is valid,
  // we won't show 73 as checked
  const selectedValidValues = selectedFilterValues.filter(value =>
    validValues.includes(value)
  )

  // The field-level checkbox should be checked if all valid values are selected
  const allSelected = validValues.every(value =>
    selectedFilterValues.includes(value)
  )

  // The field-level checkbox should be indeterminate if any valid values are selected
  const someSelected =
    !allSelected && validValues.some(value => selectedFilterValues.includes(value))

  return (
    <Accordion
      className='nested nested--level-1'
      hasBackground={false}
      key={field}
      openOnLoad={allSelected || someSelected}
      header={
        <Checkbox
          id={field}
          label={fieldName}
          checked={allSelected}
          isIndeterminate={someSelected}
          onChange={onChange}
        />
      }>
      <>
        {hasGroups ? (
          <>
            {isRequired ? null : (
              <CheckboxFilterItem
                item={'blank'}
                count={
                  counts['blank' as keyof EvaluatorFacets[keyof EvaluatorFacets]]
                }
                filteredCount={
                  filteredCounts[
                    'blank' as keyof EvaluatorFacets[keyof EvaluatorFacets]
                  ]
                }
                selected={selectedValidValues}
                field={field}
                padRight={hasGroups}
              />
            )}
            {[...fieldGroups[field as keyof typeof fieldGroups]].map(group => {
              const groupName = group[0]
              const groupItems = group[1] as (typeof FILTER_VALUES)[typeof field][]
              const groupValuesInData: (typeof FILTER_VALUES)[typeof field][] =
                groupItems.filter(item => validValues.includes(item))
              return (
                <CheckboxFilterGroup
                  field={field}
                  key={groupName}
                  groupName={groupName}
                  groupItems={groupItems}
                  counts={counts}
                  filteredCounts={filteredCounts}
                  // the keys of counts that are in this group
                  validValues={groupValuesInData}
                  // all the currently selected values for this field that are in the valid value list
                  selectedValues={selectedValidValues}
                />
              )
            })}
          </>
        ) : (
          [...FILTER_VALUES[field]].map(item => {
            return (
              <CheckboxFilterItem
                field={field}
                key={item}
                item={item as keyof EvaluatorFacets[keyof EvaluatorFacets]}
                filteredCount={
                  filteredCounts[
                    item as keyof EvaluatorFacets[keyof EvaluatorFacets]
                  ]
                }
                count={counts[item as keyof EvaluatorFacets[keyof EvaluatorFacets]]}
                selected={selectedValidValues}
              />
            )
          })
        )}
      </>
    </Accordion>
  )
}

export default CheckboxFilterSection
