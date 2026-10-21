import { Checkbox } from '@cfpb/design-system-react'
import { FILTER_VALUES } from '@src/constants/annotationLookups'
import { annotateM2FieldValue } from '@src/utils/annotations'
import { formatNumber } from '@src/utils/formatNumbers'
import getHeaderName from '@src/utils/getHeaderName'
import { useNavigate } from '@tanstack/react-router'
import type { ReactElement } from 'react'

interface CheckboxFieldFilterProperties {
  // an M2 field with predetermined list of values
  field: keyof typeof FILTER_VALUES
  // the value from the predetermined list for this checkbox
  item: (typeof FILTER_VALUES)[keyof typeof FILTER_VALUES]
  // the total number of times this value appears in all the data
  count?: number
  // the number of times this value appears in the data with
  // the currently applied filters
  filteredCount?: number
  // whether this value is one of the currently applied filters
  selected?: (typeof FILTER_VALUES)[keyof typeof FILTER_VALUES][]
  // whether to add right padding to line up the count with
  // the counts in adjacent accordion headers
  padRight?: boolean
}

export default function CheckboxFilterItem({
  field,
  count = 0,
  filteredCount = 0,
  item,
  selected = [],
  padRight = false
}: CheckboxFieldFilterProperties): ReactElement {
  const navigate = useNavigate()
  const itemName = item

  const annotated =
    itemName === 'blank'
      ? `Blank (no ${getHeaderName(field).toLowerCase()})`
      : annotateM2FieldValue(field, itemName)

  const label =
    filteredCount > 0 ? (
      <div className='label-with-count'>
        <span>{annotated}</span>
        <span className={`count ${padRight ? 'count--pad-right' : ''}`}>
          {filteredCount ? formatNumber(filteredCount) : '0'}
        </span>
      </div>
    ) : (
      <span>{annotated}</span>
    )

  const onChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const { checked } = event.currentTarget

    const vals = checked
      ? [...selected, itemName]
      : selected.filter(item => item !== itemName)
    void navigate({
      resetScroll: false,
      to: '.',
      search: (previous: Record<string, unknown>) => {
        const parameters = { ...previous }
        if (vals.length > 0) {
          parameters[field] = [...new Set(vals)].toSorted()
        } else {
          delete parameters[field]
        }
        // reset page to 1
        parameters.page = 1
        parameters.show_counts = 'true'

        return parameters
      }
    })
  }
  return (
    <Checkbox
      id={`${field}_${itemName}`}
      label={label}
      checked={selected?.includes(item)}
      className='nested'
      onChange={onChange}
      disabled={count === 0}
    />
  )
}
