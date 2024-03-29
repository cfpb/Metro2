import type { ReactElement } from 'react'

interface ErrorParameters {
  error?: Error
}

export default function ErrorComponent({
  error
}: ErrorParameters): ReactElement {
  // Todo: this component should handle access and general errors
  // Generic error content should be shown unless the error message
  // specifies an access error
  return (
    <div className='content-row'>
      {error?.message ?? 'There was a problem loading this page.'}
    </div>
  )
}
