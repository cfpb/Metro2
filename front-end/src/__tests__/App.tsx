import { screen } from '@testing-library/react'
import App from 'App'
import renderWithProviders from 'testUtils'

describe('<App />', () => {
	it('renders', async () => {
		window.history.pushState({}, 'Home', '/')
		renderWithProviders(<App />)

		await expect(screen.findByText('Metro2 Evaluator Tool')).resolves.toBeInTheDocument()
	})
})
