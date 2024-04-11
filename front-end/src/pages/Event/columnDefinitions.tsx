import { Link } from '@tanstack/react-router'
import type { ColDef, ValueFormatterParams } from 'ag-grid-community'
import type { ReactElement } from 'react'
import type EvaluatorMetadata from '../Evaluator/Evaluator'
import type Event from './Event'

const columnDefinitions: ColDef<EvaluatorMetadata>[] = [
  {
    field: 'id',
    headerName: 'Inconsistency',
    type: 'wrappableText',
    valueFormatter: ({ value }: ValueFormatterParams): string =>
      typeof value === 'string' ? value.toUpperCase() : '',
    cellRenderer: ({
      data,
      value
    }: {
      data: Event
      value: string
    }): ReactElement => (
        <Link to='evaluators/$evaluatorId' params={{ evaluatorId: data.id }}>
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
    headerName: 'Category',
    type: 'wrappableText',
    flex: 1
  },
  {
    field: 'hits',
    headerName: 'Total instances',
    type: 'formattedNumber',
    flex: 1
  },
  {
    field: 'accounts',
    headerName: 'Total accounts',
    type: 'formattedNumber',
    flex: 1
  }
]

export default columnDefinitions
