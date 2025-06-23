import { useNavigate, useSearch } from '@tanstack/react-router'
import Accordion from 'components/Accordion/Accordion'
import BooleanFilter from 'components/Filters/BooleanFilter/BooleanFilter'
import type { ReactElement } from 'react'

interface EvaluatorBooleanFilterData {
  field: 'date_closed' | 'dofd'
  header: string
  checkboxLabel?: string
}

export default function EvaluatorBooleanFilter({
  field,
  header,
  checkboxLabel
}: EvaluatorBooleanFilterData): ReactElement {
  const navigate = useNavigate()

  const queryStringValue = useSearch({
    strict: false,
    select: (search): boolean | 'any' | 'false' | 'true' | undefined => search[field]
  })

  console.log('query string value', queryStringValue)

  const onChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    console.log('on changed called')
    const { name, checked } = event.currentTarget
    let currentValue: boolean | string | undefined = queryStringValue
    console.log('starting currentValue', currentValue)

    if (checked) {
      if (currentValue === undefined) {
        currentValue = name
      } else if (currentValue !== name) {
        currentValue = 'any'
      }
    } else if (currentValue === name) {
      currentValue = undefined
    } else if (currentValue === 'any') {
      currentValue = name === 'true' ? 'false' : 'true'
    }

    console.log('ending current value', currentValue)

    void navigate({
      resetScroll: false,
      to: '.',
      search: (prev: Record<string, unknown>) => {
        const params = { ...prev }
        console.log(params)
        if (currentValue === undefined) {
          // eslint-disable-next-line @typescript-eslint/no-dynamic-delete
          if (field in params) delete params[field]
        } else {
          params[field] = currentValue
        }
        // reset page to 1
        // params.page = 1
        console.log(params)
        return params
      }
    })
  }

  return (
    <Accordion
      header={<span>{header}</span>}
      openOnLoad={queryStringValue !== undefined}>
      <BooleanFilter
        id={field}
        selected={queryStringValue}
        onChange={onChange}
        label_0={`No ${checkboxLabel}`}
        label_1={`Has a ${checkboxLabel}`}
      />
    </Accordion>
  )
}
