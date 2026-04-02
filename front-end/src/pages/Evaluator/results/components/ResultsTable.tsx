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
}

export default function EvaluatorResultsTable({
  eventData,
  data,
  fields,
  isLoading,
  isLoadingError
}: EvaluatorTableData): ReactElement {
  const navigate = useNavigate()

  const sort = useSearch({
    strict: false,
    select: search => search.sort
  })

  // Generate a column state object for the table that reflects
  // the sort state from the URL.
  // If we're in a default sort situation, where sort = activity_date
  // ascending OR there's no sort param, we also tell the table to
  // clear all other sorting because this could mean we just switched
  // tabs and we want to ensure we don't carry over sort state from one view
  // to the other.
  const columnState =
    JSON.stringify(sort) === '["activity_date"]' || sort === undefined
      ? {
          state: generateColumnStateFromSortArray(sort),
          defaultState: { sort: null }
        }
      : { state: generateColumnStateFromSortArray(sort) }

  const sortHandler = (columnState: ColumnState[] | undefined): void => {
    const currentSort = generateSortArrayFromColumnState(columnState)
    if (JSON.stringify(currentSort) !== JSON.stringify(sort)) {
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
      sortHandler={sortHandler}
      columnState={columnState}
      rows={data}
      columnDefinitions={getEvaluatorColDefs(fields, String(eventData.id))}
      NoResultsMessage={NoResultsMessage}
      isLoading={isLoading}
      isLoadingError={isLoadingError}
    />
  )
}
