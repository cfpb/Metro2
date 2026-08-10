import Loader from '@src/components/Loader/Loader'
import type { ReactElement } from 'react'

interface Properties {
  error?: Error
  loading_message?: string
}
export default function LoadingOrError({
  error,
  loading_message
}: Properties): ReactElement {
  if (error) return <>{error.message}</>
  return <Loader message={loading_message} />
}
LoadingOrError.defaultProps = {
  error: undefined
}
