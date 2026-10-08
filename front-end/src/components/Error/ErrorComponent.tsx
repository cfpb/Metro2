import type { ErrorComponentProps } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import { errors } from './ErrorList'
import ErrorMessage from './ErrorMessage'

export default function ErrorComponent({
  error
}: ErrorComponentProps): ReactElement {
  const errorType =
    error instanceof Error && error.message in errors ? error.message : '500'
  const errorObject = errors[errorType as keyof typeof errors]

  return (
    <ErrorMessage
      title={errorObject.title}
      description={errorObject.description}
      type={errorObject.errorType}
    />
  )
}
