/* eslint-disable react/jsx-handler-names */

import Accordion from 'components/Accordion/Accordion'
import type { ReactElement } from 'react'
import { IndeterminateCheckbox } from '../IndeterminateCheckbox/IndeterminateCheckbox'
import type { CheckboxItem } from './CheckboxItem'
import './NestedCheckboxGroup.less'

/**
 * NestedCheckboxGroup
 *
 * Recursively generates a group of nested checkboxes. Each parent checkbox is displayed
 * in the header of an expandable and its children in the expandable body.
 *
 * Parent checkbox state is calculated as follows:
 *    - if all the parent's descendant checkboxes are checked, parent = checked
 *    - if some but not all of the descendants are checked, parent = indeterminate
 *    - otherwise, parent = not checked
 *
 * @param {array} items An array of checkbox items, each of which might have its own
 *                      array of child checkbox items.
 *
 *                      Example array:
 *                      [
 *                        {
 *                          key: 'parent',
 *                          name: 'Parent',
 *                          onChange: parentChangeHandler
 *                          children: [
 *                              {
 *                                key: 'child1',
 *                                name: 'First child',
 *                                checked: false, // optional
 *                                onChange: childChangeHandler
 *                                children: [child items] // optional
 *                              }
 *                          ]
 *                        }
 *                      ]
 * @param {boolean} level Current level. Defaults to 1, is incremented
 *                        for children.
 *
 */

interface NestedCheckboxGroupProperties {
  items: CheckboxItem[]
  level?: number
}

export const getCheckedDescendants = (
  tree: CheckboxItem
): (boolean | undefined)[] => {
  const result = []
  const children = tree.children ?? []
  for (const child of children) {
    if (Array.isArray(child.children) && child.children.length > 0) {
      result.push(...getCheckedDescendants(child))
    } else {
      result.push(child.checked)
    }
  }
  return result
}

export default function NestedCheckboxGroup({
  items,
  level = 1
}: NestedCheckboxGroupProperties): ReactElement {
  return (
    <>
      {items.map(item => {
        const checkedDescendants = getCheckedDescendants(item)
        const allChecked = checkedDescendants.every(Boolean)
        const someChecked = allChecked || checkedDescendants.includes(true)
        return item.children && item.children.length > 0 ? (
          <Accordion
            className={`nested nested_level-${level}`}
            hasBackground={false}
            key={item.key}
            openOnLoad={level === 1 && someChecked}
            header={
              <IndeterminateCheckbox
                onChange={item.onChange}
                id={String(item.key)}
                label={item.name}
                checked={allChecked}
                // labelInline={level !== 1}
                isIndeterminate={!allChecked && someChecked}
              />
            }>
            <NestedCheckboxGroup items={item.children} level={level + 1} />
          </Accordion>
        ) : (
          <IndeterminateCheckbox
            id={String(item.key)}
            key={item.key}
            label={item.name}
            checked={item.checked}
            className='nested'
            onChange={item.onChange}
          />
        )
      })}
    </>
  )
}
