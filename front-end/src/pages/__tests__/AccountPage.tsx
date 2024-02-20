import { render, screen } from '@testing-library/react'
import AccountPage from 'pages/Account/AccountPage'

describe('<AccountPage />', () => {
	it('renders', () => {
		render(<AccountPage />)
		expect(screen.getByText('Account page')).toBeInTheDocument()
	})
})
