import Head from 'components/Head'
import type { ReactElement } from 'react'
import { useParams } from 'react-router-dom'

export default function DetailsPage(): ReactElement {
	const { id } = useParams<Record<string, string | undefined>>() 
	return (
		<>
			<Head title={id ?? ''} />
			<div>
				<h2>Evaluator {id}</h2>
			</div>
		</>
	)
}
