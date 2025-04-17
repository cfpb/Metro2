import { useNavigate, useSearch } from '@tanstack/react-router'
import Accordion from 'components/Accordion/Accordion'
import RangeFilter from 'components/Filters/RangeFilter/RangeFilter'
import type { ReactElement } from 'react'
import { getHeaderName } from 'utils/utils'
import type { EvaluatorSearch } from '../utils/searchSchema'

interface RangeFilterData {
  field: 'amt_past_due' | 'current_bal'
}

/**
 * EvaluatorRangeFilter
 *
 * Manages filtering by min and max value for a Metro 2 dollar amount field.
 *
 *   1. Retrieves min and max values for the field from the query string.
 *   2. Outputs an accordion containing range filter for the field.
 *      Accordion will be open if min or max value exists in query string.
 *   3. When min or max value is updated, calls navigate with new value.
 *
 * @param {string} field - name of a Metro 2 dollar amount field
 *
 */

export default function EvaluatorRangeFilter({
  field
}: RangeFilterData): ReactElement {
  const navigate = useNavigate()

  const [min, max] = useSearch({
    strict: false,
    select: (search): (number | undefined)[] => [
      search[`${field}_min`],
      search[`${field}_max`]
    ]
  })

  const filtered = min !== undefined || max !== undefined

  const onChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const { name, value } = event.currentTarget
    void navigate({
      resetScroll: false,
      to: '.',
      search: prev => {
        const params = { ...prev }
        const num = Number(value)
        if (value === '' || typeof num !== 'number') {
          // eslint-disable-next-line @typescript-eslint/no-dynamic-delete
          delete params[name as keyof EvaluatorSearch]
        } else {
          ;(params[name as keyof EvaluatorSearch] as number) = num
        }

        return params
      }
    })
  }

  return (
    <Accordion header={getHeaderName(field)} openOnLoad={filtered}>
      <RangeFilter id={field} min={min} max={max} onChange={onChange} />
    </Accordion>
  )
}
