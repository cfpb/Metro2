import { Alert } from '@cfpb/design-system-react'
import Loader from '@src/components/Loader/Loader'
import Table from '@src/components/Table/Table'

import { Link } from '@tanstack/react-router'

import { useAccounts } from '@src/queries/accountSearch'
import { type ReactElement } from 'react'

interface AccountSearchProperties {
  accountIds: (string | number)[]
  eventId: string | number
}

export default function AccountSearchResults({
  accountIds,
  eventId
}: AccountSearchProperties): ReactElement | null {
  // Fetch the data for these accounts
  const { data, isFetching } = useAccounts(String(eventId), accountIds.join(','))

  // Generate colDefs
  const colDefs = [
    {
      field: 'cons_acct_num',
      headerName: 'Account number',
      cellRenderer: ({ value }: { value: string }): ReactElement => (
        <Link
          to='/events/$eventId/accounts/$accountId'
          params={{ accountId: value, eventId: String(eventId) }}
          className='a-link'
          target='_blank'>
          {value}
        </Link>
      )
    }, //tooltipField: 'cons_acct_num'
    { field: 'port_type', headerName: 'Portfolio type' },
    { field: 'acct_type', headerName: 'Account type' }, //tooltipField: 'acct_type'
    { field: 'total_records', headerName: 'Number of records' },
    { field: 'total_hits', headerName: 'Total number of hits' }
  ]

  // Check if any searched-for accounts are missing from the data
  // the API returned
  const notFoundAccounts = new Set()
  let foundAccounts = new Set()

  if (data) {
    foundAccounts = new Set(data.map(acct => String(acct.cons_acct_num)))
    for (const acct of accountIds) {
      if (!foundAccounts.has(String(acct))) {
        notFoundAccounts.add(acct)
      }
    }
  }

  // Only show results when data has been returned
  const showResults = data && data.length > 0

  // Not found accounts messaging
  const showNotFoundMessage = notFoundAccounts.size > 0
  const pluralized = notFoundAccounts.size === 1 ? '' : 's'

  // Found accounts messaging
  const foundCount = foundAccounts.size
  const resultsMessage =
    foundCount > 1
      ? `Showing 1 - ${foundCount} of ${foundCount} results`
      : `Showing 1 result`

  // Show loader if data is being fetched
  if (isFetching) {
    return <Loader message='Searching for accounts' />
  }

  return (
    <>
      {showNotFoundMessage ? (
        <div className='row row--content u-mt30'>
          <Alert
            message={`At least one account couldn't be found`}
            status='warning'
            data-testid='account-not-found-message'>
            <p>
              {`If you believe you are seeing this in error, please double check the
              account number${pluralized}. If you need additional assistance, please contact an
              admin for help.`}
            </p>
            <p>
              {`We can't find account${pluralized}: ${[...notFoundAccounts].toSorted().join(', ')} `}
            </p>
          </Alert>
        </div>
      ) : null}

      {showResults ? (
        <div data-testid='account-search-results'>
          <div className='row row--action u-mt30 u-mb0'>
            <h2 className='u-mb0'>Matching account results</h2>
          </div>
          <div
            className='row row--background u-mb0'
            data-testid='account-search-results-message'>
            {resultsMessage}
          </div>
          <div className='row row--content u-mt0'>
            <Table
              rows={data}
              columnDefinitions={colDefs}
              height='full'
              isLoading={isFetching}
              resizableColumns={false}
              sizeColumnsToFit={true}
            />
          </div>
        </div>
      ) : null}
    </>
  )
}
