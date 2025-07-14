import { useNavigate, useSearch } from '@tanstack/react-router'
import type { CheckboxItem } from 'components/Filters/NestedCheckboxGroup/NestedCheckboxGroup'
import NestedCheckboxGroup from 'components/Filters/NestedCheckboxGroup/NestedCheckboxGroup'
import type { ReactElement } from 'react'

import { M2_FIELD_LOOKUPS } from '@src/constants/annotationLookups'
import fieldGroups from '@src/constants/filterFieldGroups'
import { annotateM2FieldValue } from 'utils/annotations'
import getHeaderName from 'utils/getHeaderName'
import type { EvaluatorSearch } from '../../utils/evaluatorSearchSchema'

/**
 * EvaluatorCheckboxGroup
 *
 * Implements nested checkbox group filters for a Metro2 field that has
 * a predetermined list of possible values.
 *
 * 1. Gets any applied filters for this field from search params
 * 2. Checks if this field's values are grouped and generates
 *    array of either grouped or flat checkbox items for its values
 * 3. Outputs NestedCheckboxGroup using checkbox item array
 * 4. When user checks or unchecks one of the nested checkboxes,
 *    navigates to current page with updated search params
 *
 *
 * @param {string} field - name of a Metro 2 list value field
 *
 */

interface EvaluatorCheckboxGroupProperties {
  field: keyof EvaluatorSearch
}

const canBeBlank = new Set([
  'compl_cond_cd',
  'php1',
  'pmt_rating',
  'spc_com_cd',
  'terms_freq',
  'account_holder__cons_info_ind',
  'account_holder__cons_info_ind_assoc',
  'l1__change_ind'
])

export const generateCheckboxItem = (
  field: keyof EvaluatorSearch,
  val: string,
  appliedFilters: string[]
): CheckboxItem => ({
  checked: appliedFilters.includes(String(val)),
  key: `${field}_${val}`,
  name: annotateM2FieldValue(field, val)
})

/**
 * generateGroupedCheckboxItems
 *
 * Generates an array of checkbox item groups.
 *
 * @param {string} field - name of a Metro 2 list value field
 *
 */
export const generateGroupedCheckboxItems = (
  field: keyof EvaluatorSearch,
  appliedFilters: string[]
): CheckboxItem[] =>
  // Create nested lists of options for each of the groups
  // Get the groups for this field from the fieldGroups object
  // The group name / value pairs are stored as a Map to maintain order,
  // so we need to generate an array from the groups to iterate over
  [...fieldGroups[field as keyof typeof fieldGroups]].map(item => ({
    key: `${field}_${item[0]}`, // prefix key with field because some fields share values
    name: item[0],
    children: item[1].map(val => generateCheckboxItem(field, val, appliedFilters))
  }))

export const generateFlatCheckboxItems = (
  field: keyof EvaluatorSearch,
  appliedFilters: string[]
): CheckboxItem[] => {
  const fieldValues = Object.keys(
    M2_FIELD_LOOKUPS[field as keyof typeof M2_FIELD_LOOKUPS]
  )
  return fieldValues.map(val => generateCheckboxItem(field, val, appliedFilters))
}

export default function EvaluatorCheckboxGroup({
  field
}: EvaluatorCheckboxGroupProperties): ReactElement {
  const navigate = useNavigate()

  /** Get any currently applied filters for this field from the URL  */
  const appliedFilters = useSearch({
    strict: false,
    select: (search): string[] => {
      const searchField = search[field]
      return Array.isArray(searchField) ? searchField : []
    }
  })

  /**
   * Checks if this is field where the values can be grouped
   * Generates an object containing nested entries for the field,
   * any groups it contains, and its possible values
   * */
  const groupedField = field in fieldGroups
  const currentFieldGroups = groupedField ? fieldGroups[field] : new Map()

  const fieldName = getHeaderName(field)

  const children =
    field in fieldGroups
      ? generateGroupedCheckboxItems(field, appliedFilters)
      : generateFlatCheckboxItems(field, appliedFilters)

  if (canBeBlank.has(field)) {
    children.unshift({
      key: `${field}_blank`,
      name: `Blank (no ${fieldName.toLowerCase()})`,
      checked: appliedFilters.includes('blank')
    })
  }

  const checkboxItems = [
    {
      key: field,
      name: fieldName,
      children
    }
  ]

  /**
   * When one of the nested checkboxes is checked or unchecked,
   * determine what type of checkbox it is.
   *   - Parent checkbox for the field
   *      - if checked, push all values to search params.
   *        include 'blank' if this field can be blank
   *      - if unchecked, remove field from search params
   *   - Group checkbox
   *      - if checked, push all group values to search params
   *      - if unchecked, remove all group values from params
   *   - Individual checkbox
   *      - if checked, push value to search params
   *      - if unchecked, remove value from search params
   */
  const onChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    let vals: (number | string)[] = []
    const { name, checked } = event.currentTarget
    const currentTarget = name.replace(`${field}_`, '')
    if (currentTarget === field) {
      if (checked) {
        vals = Object.keys(M2_FIELD_LOOKUPS[field as keyof typeof M2_FIELD_LOOKUPS])
        if (canBeBlank.has(field)) vals.push('blank')
      }
    } else if (groupedField && currentFieldGroups.get(currentTarget)) {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
      const groupValues: (number | string)[] = currentFieldGroups.get(currentTarget)
      vals = checked
        ? [...appliedFilters, ...groupValues]
        : appliedFilters.filter(i => !groupValues.includes(i))
    } else {
      vals = checked
        ? [...appliedFilters, currentTarget]
        : appliedFilters.filter(item => item !== currentTarget)
    }
    void navigate({
      resetScroll: false,
      to: '.',
      search: (prev: Record<string, unknown>) => {
        const params = { ...prev }
        if (vals.length > 0) {
          params[field] = [...new Set(vals)].sort()
        } else if (field in params) {
          // eslint-disable-next-line @typescript-eslint/no-dynamic-delete
          delete params[field]
        }
        // reset page to 1
        params.page = 1
        return params
      }
    })
  }

  return <NestedCheckboxGroup items={checkboxItems} onChange={onChange} />
}
