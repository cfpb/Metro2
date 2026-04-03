import { Label, TextInput } from '@cfpb/design-system-react'
import type { ReactElement } from 'react'
import { useState } from 'react'
import './RangeFilter.scss'

export type rangeValue = number | string | undefined

interface RangeFilterData {
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void
  id: string
  initialMin?: rangeValue
  initialMax?: rangeValue
}

const onKeyDown = (event: React.KeyboardEvent<HTMLInputElement>): void => {
  if (event.key === 'Enter') {
    const target = event.target as HTMLInputElement
    target.blur()
  }
}

export default function RangeFilter({
  id,
  initialMin,
  initialMax,
  onChange
}: RangeFilterData): ReactElement {
  const [min, setMin] = useState(initialMin ?? '')
  const [max, setMax] = useState(initialMax ?? '')

  const onMinChange = (event: React.ChangeEvent<HTMLInputElement>): void =>
    setMin(event.target.value)

  const onMaxChange = (event: React.ChangeEvent<HTMLInputElement>): void =>
    setMax(event.target.value)

  const onBlur = (event: React.ChangeEvent<HTMLInputElement>): void => {
    onChange(event)
  }

  return (
    <div className='range-filter'>
      <div className='range-input'>
        <Label htmlFor={`${id}_min`}>Min</Label>
        <TextInput
          name={`${id}_min`}
          id={`${id}_min`}
          type='number'
          min='0'
          step='1'
          value={min}
          onBlur={onBlur}
          onChange={onMinChange}
          onKeyDown={onKeyDown}
        />
      </div>
      <div className='range-input'>
        <Label htmlFor={`${id}_max`}>Max</Label>
        <TextInput
          name={`${id}_max`}
          id={`${id}_max`}
          type='number'
          min='0'
          step='1'
          value={max}
          onBlur={onBlur}
          onChange={onMaxChange}
          onKeyDown={onKeyDown}
        />
      </div>
    </div>
  )
}
