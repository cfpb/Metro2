import type { ReactElement } from 'react'

import { Checkbox } from 'design-system-react'

interface BooleanFilterData {
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
  selected?: boolean | '' | 'any' | 'false' | 'true' | undefined
  id: string
  label_0?: string
  label_1?: string
}

export default function BooleanFilter({
  onChange,
  selected,
  id,
  label_0,
  label_1
}: BooleanFilterData): ReactElement {
  return (
    <div>
      <Checkbox
        id={`${id}_false`}
        checked={selected === 'false' || selected === false || selected === 'any'}
        name='false'
        label={label_0 ?? 'No value'}
        onChange={onChange}
      />
      <Checkbox
        id={`${id}_true`}
        checked={selected === 'true' || selected === true || selected === 'any'}
        name='true'
        label={label_1 ?? 'Has value'}
        onChange={onChange}
      />
    </div>
  )
}
