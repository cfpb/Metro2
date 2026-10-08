import Accordion from '@src/components/Accordion/Accordion'
import type { booleanFilterValue } from '@src/components/Filters/BooleanFilter/BooleanFilter'
import BooleanFilter from '@src/components/Filters/BooleanFilter/BooleanFilter'
import type { EvaluatorSearch } from '@src/pages/Evaluator/utils/evaluatorSearchSchema'
import { useNavigate, useSearch } from '@tanstack/react-router'
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
    select: search => search[field as keyof EvaluatorSearch]
  })

  const onChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const { name, checked } = event.currentTarget
    let currentValue = queryStringValue

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

    void navigate({
      resetScroll: false,
      to: '.',
      search: (previous: Record<string, unknown>) => {
        const parameters = { ...previous }
        if (currentValue === undefined) {
          delete parameters[field]
        } else {
          parameters[field] = currentValue
        }
        // reset page to 1
        parameters.page = 1
        return parameters
      }
    })
  }

  return (
    <Accordion
      header={<span>{header}</span>}
      openOnLoad={queryStringValue !== undefined}>
      <BooleanFilter
        id={field}
        selected={queryStringValue as booleanFilterValue}
        onChange={onChange}
        label_0={`No ${checkboxLabel}`}
        label_1={`Has a ${checkboxLabel}`}
      />
    </Accordion>
  )
}
