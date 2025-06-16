import { notFound } from '@tanstack/react-router'

/**
 * Fetches data from the API using provided URL.
 * Returns JSON from successful requests and throws
 * appropriate errors for unsuccessful ones.
 */
const fetchData = async <TData>(
  url: string,
  dataType: string,
  delay?: number
): Promise<TData> => {
  try {
    // Fetch data from URL.
    // If response is successful, return JSON.
    // If unsuccessful, throw an error with the response
    // status (404, 500, etc) as its message.
    const response = await fetch(url)
    if (delay) {
      // Dev hack to show loading view
      // eslint-disable-next-line no-promise-executor-return
      await new Promise(r => setTimeout(r, delay))
    }
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

export default fetchData
