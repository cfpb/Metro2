import type { ReactElement } from 'react'

import { Checkbox } from '@cfpb/design-system-react'

export type booleanFilterValue = boolean | '' | 'any' | 'false' | 'true' | undefined

interface BooleanFilterData {
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
  selected?: booleanFilterValue
  id: string
  label_0?: string
  label_1?: string
}

export default function BooleanFilter({
  onChange,
  selected,
  id,
  label_0 = 'No value',
  label_1 = 'Has value'
}: BooleanFilterData): ReactElement {
  return (
    <div>
      <Checkbox
        id={`${id}_false`}
        checked={
          selected !== undefined && ['false', false, 'any'].includes(selected)
        }
        name='false'
        label={label_0}
        onChange={onChange}
      />
      <Checkbox
        id={`${id}_true`}
        checked={selected !== undefined && ['true', true, 'any'].includes(selected)}
        name='true'
        label={label_1}
        onChange={onChange}
      />
    </div>
  )
}
