import Table from 'components/Table/Table'
import type { ReactElement } from 'react'
import { useMemo } from 'react'
import type AccountRecord from 'types/AccountRecord'
import type Event from 'types/Event'
import getEvaluatorColDefs from '../utils/getColDefs'
import NoResultsMessage from './NoResultsMessage/NoResultsMessage'

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
  const columnDefinitions = useMemo(
    () => getEvaluatorColDefs(fields, String(eventData.id)),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  )
  return (
    <Table
      rows={data}
      columnDefinitions={columnDefinitions}
      NoResultsMessage={NoResultsMessage}
      isLoading={isLoading}
      isLoadingError={isLoadingError}
    />
  )
}
