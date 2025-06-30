import { notFound } from '@tanstack/react-router'

/**
 * fetchData()
 *
 * Fetches data from the API using provided URL.
 * Returns JSON from successful requests and throws
 * appropriate errors for unsuccessful ones.
 *
 * @param {string} url - url for an API endpoint
 * @param {string} dataType - type of data (ie, 'event' or 'account') being
 *                            fetched from API. This is used to determine
 *                            error message text if request fails
 * @param {number} delay - an optional parameter for use in local testing.
 *                         Uncomment this param and the associated if clause
 *                         and pass a number in milliseconds to delay the
 *                         request completion
 * @returns {Promise} - returns response or throws error
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
    // Dev hack: uncomment & pass value to delay request & show loading view
    if (delay) {
      // eslint-disable-next-line no-promise-executor-return
      await new Promise(r => setTimeout(r, delay))
    }
    if (response.ok) return (await response.json()) as TData
    // const errorBody = (await response.json()) as JSON
    // throw new Error(`${response.status}`, { cause: errorBody })
    throw new Error(String(response.status))
  } catch (error) {
    // Throw NotFound error to handle 404s in NotFound component
    // All other errors will be caught by ErrorComponent
    const message = error instanceof Error ? error.message : ''
    if (message === '404' && dataType !== 'hits')
      notFound({ throw: true, data: dataType })

    throw new Error(message)
  }
}

export default fetchData
