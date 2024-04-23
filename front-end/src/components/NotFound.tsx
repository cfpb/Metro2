import type { NotFoundError } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import { notFoundErrors } from './ErrorList'
import ErrorMessage from './ErrorMessage'

export default function NotFound({ data }: NotFoundError): ReactElement {
  // Data prop should reflect the request that threw the not found error:
  // 'account', 'evaluator', or 'event'

  // the "event" message is the default not found error message
  let eventError = notFoundErrors.event

  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
  const errorType = data?.data

  if (errorType in notFoundErrors){
    eventError = notFoundErrors[errorType as keyof typeof notFoundErrors]
  }

  return (
    <ErrorMessage
    title={eventError.title}
    description={eventError.description}
    cta1={eventError.cta1}
    cta2={eventError.cta2}
    />
  )
}