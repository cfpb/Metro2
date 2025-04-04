import { Label, TextInput } from 'design-system-react'
import type { ReactElement } from 'react'
import './RangeFilter.less'

interface RangeFilterData {
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
  id: string
  min?: number
  max?: number
}

export default function RangeFilter({
  id,
  min,
  max,
  onChange
}: RangeFilterData): ReactElement {
  return (
    <div className='range-filter'>
      <div className='range-input'>
        <Label htmlFor={`${id}_min`}>Min</Label>
        <TextInput
          name={`${id}_min`}
          id={`${id}_min`}
          type='number'
          // placeholder='min'
          defaultValue={min}
          onBlur={onChange}
        />
      </div>
      <div className='range-input'>
        <Label htmlFor={`${id}_max`}>Max</Label>
        <TextInput
          name={`${id}_max`}
          id={`${id}_max`}
          type='number'
          // placeholder='max'
          defaultValue={max}
          onBlur={onChange}
        />
      </div>
    </div>
  )
}
