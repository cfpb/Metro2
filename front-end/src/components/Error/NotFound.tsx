import type { ReactElement } from 'react'
import { notFoundErrors } from './ErrorList'
import ErrorMessage from './ErrorMessage'
import { NotFoundRouteProps } from '@tanstack/react-router'

  export default function NotFoundMessage({data}: NotFoundRouteProps): ReactElement {
    // If the NotFound error was thrown in the data fetch process, we send a data prop
    // indicating the route type that caused the error (`event`, `evaluator`, or `account`),
    // and use that value to look up the appropriate error messaging.
    // 
    // If that data isn't available because the error was thrown by the app, we show the
    // default `event` error message instead.
  
    const errorType = typeof data === 'string' && data in notFoundErrors ? data : 'event'
    const errorData = notFoundErrors[errorType as keyof typeof notFoundErrors]

  return <ErrorMessage title={errorData.title} description={errorData.description} />
}
