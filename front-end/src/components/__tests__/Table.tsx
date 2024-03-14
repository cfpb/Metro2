import type { ColDef, ValueFormatterParams } from 'ag-grid-community'
import { render, screen } from '@testing-library/react'
import Table from '../Table/Table'

interface CarManufacturer {
  company: string,
  model: string,
  start_date: string,
  end_date: string,
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
		type: 'wrappableText',
	},
  {
		field: 'model',
		headerName: 'Model name',
	},
  {
		field: 'start_date',
		headerName: 'Production begins',
	},
  {
		field: 'end_date',
		headerName: 'Production ends',
	},
	{
		field: 'number_produced',
		headerName: 'Number produced',
		type: 'formattedNumber'
	}
]

describe('<Table />', () => {
	it('renders with default props', () => {
	  render(<Table<CarManufacturer> rows={ data } columnDefinitions={ colDefs }/>)
    const container = screen.getByTestId('data-grid-container')
    expect(container).toBeVisible()
    expect(container).toHaveClass('data-grid-container--fixed-height')
	})
})
