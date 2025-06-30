import { Link } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import './NoResultsMessage.less'

interface NoResultsMessageProps {
  isError?: boolean
}

export default function NoResultsMessage({
  isError
}: NoResultsMessageProps): ReactElement {
  return (
    <div className='no-results-message block' data-testid='no-results-message'>
      {isError ? (
        <>
          <h3 className=''>Something went wrong</h3>
          <p className='u-mt30'>
            There is a problem showing these results. Please try reloading the page
            to see if that fixes the problem. If you need additional assistance,
            please contact an administrator for help.
          </p>
        </>
      ) : (
        <>
          <h3 className=''>No results found</h3>
          <p className='u-mt30'>
            There are no results matching your filter criteria. Try removing or
            changing filters to show more results.
          </p>
          <p className='block'>
            <Link
              to='.'
              resetScroll={false}
              search={(prev): object => ({
                page: 1,
                page_size: prev.page_size,
                view: 'all'
              })}
              style={{ pointerEvents: 'auto' }}
              data-testid='no-results-message_clear-filters'>
              Clear all filters
            </Link>
          </p>
        </>
      )}
    </div>
  )
}
