import { useNavigate, useSearch } from '@tanstack/react-router'
import type { CheckboxItem } from 'components/Filters/NestedCheckboxGroup/CheckboxItem'
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

const canBeBlankFields = new Set([
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
  appliedFilters: string[],
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
): CheckboxItem => ({
  checked: appliedFilters.includes(String(val)),
  key: `${field}_${val}`,
  name: annotateM2FieldValue(field, val),
  onChange
})

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
   * Gets any groupings for this field's values.
   */
  const groupedField = field in fieldGroups
  const currentFieldGroups = groupedField ? fieldGroups[field] : new Map()

  /**
   * Event handlers
   */

  /**
   * After a checkbox is changed, receives updated list
   * of values for the field, generates updated query params,
   * and calls navigate with new params.
   */
  const updateNavigation = (fieldValue: unknown[]): void => {
    void navigate({
      resetScroll: false,
      to: '.',
      search: (prev: Record<string, unknown>) => {
        const params = { ...prev }
        if (fieldValue.length > 0) {
          params[field] = [...new Set(fieldValue)].sort()
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

  /**
   * When parent checkbox for the field is changed:
   *   - if checked, update navigation with all possible values
   *     for the field
   *   - if unchecked, update navigation with empty array
   */
  const onFieldCheckboxChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    const { checked } = event.currentTarget
    let vals: string[] = []
    if (checked) {
      vals = Object.keys(M2_FIELD_LOOKUPS[field as keyof typeof M2_FIELD_LOOKUPS])
      if (canBeBlankFields.has(field)) vals.push('blank')
    }
    updateNavigation(vals)
  }

  /**
   * When a group checkbox is changed:
   *   - if checked, update navigation with current list of
   *     values for the field + all possible values for group
   *   - if unchecked, remove all group values from current value list
   */
  const onGroupCheckboxChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    const { name, checked } = event.currentTarget
    const currentTarget = name.replace(`${field}_`, '')
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
    const groupValues: (number | string)[] = currentFieldGroups.get(currentTarget)
    const vals = checked
      ? [...appliedFilters, ...groupValues]
      : appliedFilters.filter(i => !groupValues.includes(i))
    updateNavigation(vals)
  }

  /**
   * When an individual checkbox is changed:
   *   - if checked, add this value to list of applied values
   *     from query params and update navigation
   *   - if unchecked, remove value from list of applied values
   *     and update navigation
   */
  const onIndividualCheckboxChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    const { name, checked } = event.currentTarget
    const currentTarget = name.replace(`${field}_`, '')
    const vals: (number | string)[] = checked
      ? [...appliedFilters, currentTarget]
      : appliedFilters.filter(item => item !== currentTarget)
    updateNavigation(vals)
  }

  /**
   * Generate list of checkbox items for this field
   */
  let children: CheckboxItem[] = []

  if (field in fieldGroups) {
    // If the field has groups, generate checkbox items for each group.
    // Each group item gets an array of child items for its values.
    children = [...fieldGroups[field as keyof typeof fieldGroups]].map(item => ({
      key: `${field}_${item[0]}`, // prefix key with field because some fields share values
      name: item[0],
      onChange: onGroupCheckboxChange,
      children: item[1].map(val =>
        generateCheckboxItem(field, val, appliedFilters, onIndividualCheckboxChange)
      )
    }))
  } else {
    // If there are no groups, generate an array of items for the field's values.
    const values = Object.keys(
      M2_FIELD_LOOKUPS[field as keyof typeof M2_FIELD_LOOKUPS]
    )
    children = values.map(val =>
      generateCheckboxItem(field, val, appliedFilters, onIndividualCheckboxChange)
    )
  }

  // Get display name for field
  const fieldName = getHeaderName(field)

  // If the field can be blank, add a checkbox item for blank values.
  if (canBeBlankFields.has(field)) {
    children.unshift({
      key: `${field}_blank`,
      name: `Blank (no ${fieldName.toLowerCase()})`,
      checked: appliedFilters.includes('blank')
    })
  }

  // Create a checkbox item for the field with the child array generated above
  const items = [
    {
      key: field,
      name: fieldName,
      onChange: onFieldCheckboxChange,
      children
    }
  ]

  return <NestedCheckboxGroup items={items} />
}
