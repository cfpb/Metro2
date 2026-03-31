import {
  generateColumnStateFromSortArray,
  generateSortArrayFromColumnState
} from '@src/utils/sortState'
import { useNavigate, useSearch } from '@tanstack/react-router'
import Table from 'components/Table/Table'
import type { ReactElement } from 'react'
import type AccountRecord from 'types/AccountRecord'
import type Event from 'types/Event'
import getEvaluatorColDefs from '../utils/getColDefs'
import NoResultsMessage from './NoResultsMessage/NoResultsMessage'

import type { ColumnState } from 'ag-grid-community'

interface EvaluatorTableData {
  eventData: Event
  data: AccountRecord[]
  fields: string[]
  isLoading?: boolean
  isLoadingError?: boolean
  sortOnServer?: boolean
}

export default function EvaluatorResultsTable({
  eventData,
  data,
  fields,
  isLoading,
  isLoadingError,
  sortOnServer = false
}: EvaluatorTableData): ReactElement {
  const navigate = useNavigate()

  console.log('sort on', sortOnServer)
  const sort = useSearch({
    strict: false,
    select: search => search.sort
  })

  const sortHandler = (columnState: ColumnState[] | undefined): void => {
    console.log('here')
    const currentSort = generateSortArrayFromColumnState(columnState)
    if (JSON.stringify(currentSort) !== JSON.stringify(sort)) {
      console.log('nav')
      void navigate({
        to: '.',
        resetScroll: false,
        search: (prev: Record<string, unknown>) => {
          return {
            ...prev,
            page: 1,
            sort:
              Array.isArray(currentSort) && currentSort.length > 0
                ? currentSort
                : 'activity_date'
          }
        }
      })
    }
  }
  return (
    <Table
      sortExternally
      sortHandler={sortHandler}
      sortedColumns={generateColumnStateFromSortArray(sort)}
      rows={data}
      columnDefinitions={getEvaluatorColDefs(fields, String(eventData.id))}
      NoResultsMessage={NoResultsMessage}
      isLoading={isLoading}
      isLoadingError={isLoadingError}
    />
  )
}
