import { screen, within } from '@testing-library/react'
import getHeaderName from 'utils/getHeaderName'
import M2_FIELD_NAMES from '../../../constants/m2FieldNames'
import renderWithProviders from '../../../testUtils'
import AccountSummary from './Summary'

const defaultData = {
  cons_acct_num: '999999999',
  account_activity: [
    {
      activity_date: '2023-11-01',
      date_open: '2014-12-02',
      port_type: 'I', // Installment
      acct_type: '00', // Auto
      terms_dur: '74',
      terms_freq: 'M' // Monthly
    }
  ],
  inconsistencies: ['Test-Eval-1', 'Test-Eval-2']
}

const eventData = {
  id: 1,
  name: 'test event',
  date_range_start: '05-01-22',
  date_range_end: '05-01-23',
  inconsistencies: ['Test-Eval-1'],
  evaluators: [
    {
      id: 'Test-Eval-1',
      description: 'Evaluator description.',
      hits: 1000,
      accounts_affected: 500,
      inconsistency_start: '',
      inconsistency_end: '',
      long_description: 'Long description',
      fields_used: [],
      fields_display: []
    }
  ]
}

describe('<AccountSummary />', () => {
  it('should render inconsistencies when present', async () => {
    renderWithProviders(
      <AccountSummary accountData={defaultData} eventData={eventData} />
    )
    const inconsistencySection = await screen.findByTestId('inconsistencies')
    expect(inconsistencySection).toBeInTheDocument()
    const inconsistencyLinks = within(inconsistencySection).getAllByRole('link')
    expect(inconsistencyLinks).toHaveLength(2)
    expect(inconsistencyLinks[0]).toHaveTextContent('Test-Eval-1')
    expect(inconsistencyLinks[0]).toHaveAttribute(
      'href',
      '/events/1/evaluators/Test-Eval-1?page=1&view=sample&page_size=20'
    )
    expect(inconsistencyLinks[1]).toHaveTextContent('Test-Eval-2')
    expect(inconsistencyLinks[1]).toHaveAttribute(
      'href',
      '/events/1/evaluators/Test-Eval-2?page=1&view=sample&page_size=20'
    )
  })

  it('should not render inconsistency section without inconsistencies', async () => {
    const accountData = {
      cons_acct_num: defaultData.cons_acct_num,
      account_activity: defaultData.account_activity,
      inconsistencies: []
    }
    renderWithProviders(
      <AccountSummary accountData={accountData} eventData={eventData} />
    )
    const detailsSection = await screen.findByTestId('details')
    expect(detailsSection).toBeInTheDocument()
    const inconsistencySection = screen.queryByTestId('inconsistencies')
    expect(inconsistencySection).not.toBeInTheDocument()
  })

  it('renders field names, summary values, and definitions', async () => {
    renderWithProviders(
      <AccountSummary accountData={defaultData} eventData={eventData} />
    )
    const detailsSection = await screen.findByTestId('details')
    expect(detailsSection).toBeInTheDocument()
    expect(
      screen.getByText(`${getHeaderName('date_open', M2_FIELD_NAMES)}:`)
    ).toBeInTheDocument()
    expect(screen.getByText('12/02/14')).toBeInTheDocument()
    expect(
      screen.getByText(`${getHeaderName('terms_dur', M2_FIELD_NAMES)}:`)
    ).toBeInTheDocument()
    expect(screen.getByText('74')).toBeInTheDocument()
    expect(
      screen.getByText(`${getHeaderName('port_type', M2_FIELD_NAMES)}:`)
    ).toBeInTheDocument()
    expect(screen.getByText('Installment')).toBeInTheDocument()
    expect(
      screen.getByText(`${getHeaderName('acct_type', M2_FIELD_NAMES)}:`)
    ).toBeInTheDocument()
    expect(screen.getByText('Auto')).toBeInTheDocument()
    expect(
      screen.getByText(`${getHeaderName('terms_freq', M2_FIELD_NAMES)}:`)
    ).toBeInTheDocument()
    expect(screen.getByText('Monthly')).toBeInTheDocument()
  })

  it('renders summary values from first activity record if multiple records', async () => {
    const data = {
      cons_acct_num: defaultData.cons_acct_num,
      inconsistencies: defaultData.inconsistencies,
      account_activity: [
        { ...defaultData.account_activity[0], terms_dur: 'LOC' },
        { ...defaultData.account_activity[0], terms_dur: 'REV' }
      ]
    }
    renderWithProviders(<AccountSummary accountData={data} eventData={eventData} />)
    const detailsSection = await screen.findByTestId('details')
    expect(detailsSection).toBeInTheDocument()
    expect(within(detailsSection).getByText('LOC')).toBeInTheDocument()
    expect(within(detailsSection).queryByText('REV')).not.toBeInTheDocument()
  })
})
