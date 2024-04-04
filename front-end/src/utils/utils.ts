import { notFound } from '@tanstack/react-router'
import { M2_FIELD_LOOKUPS } from './constants'

/**
 * Takes an id and value for a Metro2 field,
 * accesses the lookup for the field's code definitions,
 * and returns either the definition corresponding with
 * the value provided for the field or undefined.
 */
export default function getM2CodeDefinition(
  fieldId: string,
  fieldValue?: number | string | null
): string | undefined {
  if (fieldValue != null && fieldId in M2_FIELD_LOOKUPS) {
    const lookup = M2_FIELD_LOOKUPS[fieldId as keyof typeof M2_FIELD_LOOKUPS]
    if (fieldValue in lookup) {
      return lookup[fieldValue as keyof typeof lookup]
    }
  }
  return undefined
}

/**
 * Fetches data from the API using provided URL.
 * Returns JSON from successful requests and throws
 * appropriate errors for unsuccessful ones.
 */
export const fetchData = async <TData>(
  url: string,
  dataType: string
): Promise<TData> => {
  try {
    // Fetch data from URL.
    // If response is successful, return JSON.
    // If unsuccessful, throw an error with the response
    // status (404, 500, etc) as its message.

    // Temporary hack to show loading view
    // eslint-disable-next-line no-promise-executor-return
    await new Promise(r => setTimeout(r, 2000))

    const response = await fetch(url)
    if (response.ok) return (await response.json()) as TData
    throw new Error(String(response.status))
  } catch (error) {
    // Throw NotFound error to handle 404s in NotFound component
    // All other errors will be caught by ErrorComponent
    const message = error instanceof Error ? error.message : ''
    if (message === '404') notFound({ throw: true, data: dataType })
    throw new Error(message)
  }
}
