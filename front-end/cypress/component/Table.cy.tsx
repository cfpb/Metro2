import Table from '@src/components/Table/Table'
import type { ColDef } from 'ag-grid-community'

interface CarManufacturer {
  company: string
  model: string
  start_date: string
  end_date: string
  number_produced: number
}

const data = [
  {
    company: 'Tucker Corporation',
    model: 'Tucker 48',
    start_date: '1947',
    end_date: '1948',
    number_produced: 50
  },
  {
    company: 'Gordon Keeble',
    model: 'GK1',
    start_date: '1964',
    end_date: '1967',
    number_produced: 100
  },
  {
    company: 'DeLorean Motor Company',
    model: 'DMC-12',
    start_date: '1981',
    end_date: '1982',
    number_produced: 9000
  }
]

const colDefs: ColDef<CarManufacturer>[] = [
  {
    field: 'company',
    headerName: 'Company name',
    type: 'wrappableText'
  },
  {
    field: 'model',
    headerName: 'Model name'
  },
  {
    field: 'start_date',
    headerName: 'Production begins'
  },
  {
    field: 'end_date',
    headerName: 'Production ends'
  },
  {
    field: 'number_produced',
    headerName: 'Number produced',
    type: 'formattedNumber'
  }
]

describe('Table.cy.tsx', () => {
  it('renders', () => {
    cy.mountWithProviders(
      <Table<CarManufacturer>
        rows={data}
        columnDefinitions={colDefs}
        defaultSort={['company']}
      />
    )
    cy.findByTestId('data-grid-container').should('be.visible')
  })
})
