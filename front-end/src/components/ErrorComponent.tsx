import type { ErrorComponentProps } from '@tanstack/react-router'
import type { ReactElement } from 'react'

export default function ErrorComponent({
  error
}: ErrorComponentProps): ReactElement {
  const message =
    error instanceof Error ? error.message : 'There was a problem loading this page.'
  return <div className='content-row'>{message}</div>
}
