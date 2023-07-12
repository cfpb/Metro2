import type { ReactElement } from 'react'

export default function TestPage(): ReactElement {
	return (
		<>
			<div data-testid='header'>
				<h2>Test page</h2>
			</div>
		</>
	)
}
