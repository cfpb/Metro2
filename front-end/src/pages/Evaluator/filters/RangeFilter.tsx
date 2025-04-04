import { useNavigate, useSearch } from '@tanstack/react-router'
import Accordion from 'components/Accordion/Accordion'
import RangeFilter from 'components/Filters/RangeFilter/RangeFilter'
import type { ReactElement } from 'react'
import { getHeaderName } from 'utils/utils'
import type { EvaluatorSearch } from '../utils/searchSchema'

interface RangeFilterData {
  field: keyof EvaluatorSearch
}

export default function EvaluatorRangeFilter({
  field
}: RangeFilterData): ReactElement {
  const navigate = useNavigate()

  const [min, max] = useSearch({
    strict: false,
    select: (search): number[] => [search[`${field}_min`], search[`${field}_max`]]
  })

  const onChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const { name, value } = event.currentTarget
    void navigate({
      resetScroll: false,
      to: '.',
      search: prev => {
        const params = { ...prev }
        if (value === null || value === undefined || value === '') {
          delete params[name]
        } else {
          params[name] = Number(value)
        }

        return params
      }
    })
  }

  const filtered = min !== undefined || max !== undefined

  return (
    <Accordion header={getHeaderName(field)} openOnLoad={filtered}>
      <RangeFilter id={field} min={min} max={max} onChange={onChange} />
    </Accordion>
  )
}
