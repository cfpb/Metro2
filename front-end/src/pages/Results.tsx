import type { ReactElement } from 'react'
import Head from 'components/Head'

export default function ResultsPage(): ReactElement {
	return (
		<>
			<Head title='Results' />
			<div data-testid='header'>
				<h2>Results</h2>		
			</div>
		</>
	)
}
