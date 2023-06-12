import Head from 'components/Head'
import type { ReactElement } from 'react'

export default function HomePage(): ReactElement {
	return (
		<>
			<Head title='Metro 2' />
			<div data-testid='header'>
				<h2>Your cases</h2>
			</div>
		</>
	)
}
