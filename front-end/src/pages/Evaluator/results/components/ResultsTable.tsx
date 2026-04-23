import Table from '@src/components/Table/Table'
import type AccountRecord from '@src/types/AccountRecord'
import type Event from '@src/types/Event'
import type { ReactElement } from 'react'
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
  return (
    <Table
      defaultSort={['activity_date']}
      rows={data}
      columnDefinitions={getEvaluatorColDefs(fields, String(eventData.id))}
      NoResultsMessage={NoResultsMessage}
      isLoading={isLoading}
      isLoadingError={isLoadingError}
      isSortedOnServer={true}
    />
  )
}
