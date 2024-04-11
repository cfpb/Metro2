import type { ReactElement } from 'react'
import { getM2Definition } from 'utils/utils'

interface AnnotationProperties {
  field: string | undefined
  value: number | string | null | undefined
}

export default function AnnotatedText({
  field,
  value
}: AnnotationProperties): ReactElement | null {
  if (value == null || field == null) return null

  const definition = getM2Definition(field, value)
  if (definition) {
    return (
      <span>
        {value} ({definition})
      </span>
    )
  } 
    return <span>{value}</span>
  
}
