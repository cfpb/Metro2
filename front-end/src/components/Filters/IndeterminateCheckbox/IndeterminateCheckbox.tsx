import type { ChangeEvent, ReactElement, ReactNode } from 'react'
import { useEffect, useRef } from 'react'

import { Label } from 'design-system-react'
import './IndeterminateCheckbox.less'

/**
 * IndeterminateCheckbox
 *
 * Based on the checkbox component in the DSR:
 *   https://github.com/cfpb/design-system-react/blob/main/src/components/Checkbox/Checkbox.tsx
 *
 * Adds an indeterminate state, illustrated by a minus sign.
 * Used with nested checkboxes to indicate that children are partially selected.
 *
 * An HTML checkbox can be marked as indeterminate by applying the indeterminate property
 * using JavaScript. Indeterminate state is visual only.
 *
 * @param {boolean} isIndeterminate - whether the indeterminate property should be
 *                                    set to true for this checkbox
 * ...
 *
 */

export interface CheckboxProperties {
  /** Unique identifier for this checkbox */
  id: number | string
  /** Text that appears next to the checkbox for clarification of purpose */
  label: ReactNode
  /** Additional CSS classes applied to the checkbox's wrapper element */
  className?: string
  /** Is checkboxed checked? */
  checked?: boolean
  /** Additional CSS classes that will be applied to checkbox input element */
  inputClassName?: string
  /** Apply indeterminate attribute to checkbox? */
  isIndeterminate?: boolean
  /** Apply the "Large" styles for this element? */
  isLarge?: boolean
  /** Additional CSS classes that will be applied to checkbox label element */
  labelClassName?: string
  /** Removes/Adds 'label__heading' class to the Label * */
  labelInline?: boolean
  /** A name for this checkbox's value that can be referenced in javascript */
  name?: string
  /** Is this checkbox disabled? */
  disabled?: boolean
  /** An event handler function that will be called when the checkbox's value is changed  */
  onChange?: (event: ChangeEvent<HTMLInputElement>) => void
  /** Border status */
  status?: 'error' | 'success' | 'warning'
}

const containerBaseStyles = ['m-form-field m-form-field__checkbox']

const borderStatus = {
  success: 'm-form-field__checkbox__success',
  warning: 'm-form-field__checkbox__warning',
  error: 'm-form-field__checkbox__error'
}

export function IndeterminateCheckbox({
  id,
  label,
  className,
  inputClassName,
  labelClassName = '',
  checked = false,
  disabled = false,
  isIndeterminate = false,
  isLarge = false,
  labelInline = true, // 'true' REMOVES the a.label__heading class
  name,
  onChange,
  status,
  ...properties
}: CheckboxProperties & JSX.IntrinsicElements['input']): ReactElement {
  const onChangeHandler = (event: ChangeEvent<HTMLInputElement>): void => {
    onChange?.(event)
  }

  const ref = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (ref.current) {
      ref.current.indeterminate = isIndeterminate
    }
  })

  const containerClasses = [
    ...containerBaseStyles,
    isLarge ? 'm-form-field__lg-target' : '',
    status && status in borderStatus ? borderStatus[status] : '',
    isIndeterminate ? 'indeterminate' : '',
    className
  ]

  return (
    <div className={containerClasses.join(' ')} data-testid={`${id}-container`}>
      <input
        id={id}
        type='checkbox'
        checked={checked}
        name={name ?? id}
        ref={ref}
        disabled={disabled}
        onChange={onChangeHandler}
        {...properties}
        data-testid={`${id}-input`}
        className={['a-checkbox', inputClassName].join(' ')}
      />
      <Label
        id={`${id}-label`}
        className={labelClassName}
        htmlFor={id}
        inline={labelInline}>
        {label}
      </Label>
    </div>
  )
}

export default IndeterminateCheckbox
