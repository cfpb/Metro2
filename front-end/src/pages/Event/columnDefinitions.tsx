import { Link } from '@tanstack/react-router'
import type { ColDef, ValueFormatterParams } from 'ag-grid-community'
import type { ReactElement } from 'react'
import type EvaluatorMetadata from '../Evaluator/Evaluator'

const getColumnDefinitions = (eventId: string): ColDef<EvaluatorMetadata>[] => [
  {
    field: 'id',
    headerName: 'Evaluator',
    type: 'wrappableText',
    valueFormatter: ({ value }: ValueFormatterParams): string =>
      typeof value === 'string' ? value.toUpperCase() : '',
    cellRenderer: ({
      data,
      value
    }: {
      data: EvaluatorMetadata
      value: string
    }): ReactElement => (
      <Link
        to='/events/$eventId/evaluators/$evaluatorId'
        params={{ evaluatorId: data.id, eventId }}>
        {value}
      </Link>
    )
  },
  {
    field: 'description',
    headerName: 'Description',
    type: 'wrappableText',
    flex: 3
  },
  {
    field: 'category',
    headerName: 'Categories',
    type: 'wrappableText',
    flex: 1,
    cellRenderer: ({ value }: { value: string[] }): ReactElement => (
      <>
        {value.map(item => (
          <div key={item}>{item}</div>
        ))}
      </>
    )
  },
  {
    field: 'hits',
    headerName: 'Total instances',
    type: 'formattedNumber',
    flex: 1
  },
  {
    field: 'accounts_affected',
    headerName: 'Total accounts',
    type: 'formattedNumber',
    flex: 1
  }
]
export default getColumnDefinitions
