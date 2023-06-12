import { render, screen } from '@testing-library/react'
import HeaderNavbar from '../HeaderNavbar'

describe('<HeaderNavbar />', () => {
	it('displays logo', () => {
		render(<HeaderNavbar />)
		const logo = screen.getByRole('img')

		expect(logo).toHaveAttribute('src', '/images/logo_237x50@2x.png')
	})
})
