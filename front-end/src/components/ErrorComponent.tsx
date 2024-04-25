import type { ReactElement } from 'react'
import { errors } from './ErrorList'
import ErrorMessage from './ErrorMessage'

export default function ErrorComponent({ error }: { error: Error }): ReactElement {
  const errorType = error.message in errors ? error.message : '500'
  const errorObj = errors[errorType as keyof typeof errors]

  return (
    <ErrorMessage
    title={errorObj.title}
    description={errorObj.description}
    cta1={errorObj.cta1}
    cta2={errorObj.cta2} />
  )
}