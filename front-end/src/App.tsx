import LoadingOrError from 'components/LoadingOrError'
import type { ReactElement } from 'react'
import { lazy, Suspense } from 'react'
import { HashRouter, Route, Routes } from 'react-router-dom'

const Results = lazy(async () => import('pages/Results'))
const Evaluator = lazy(async () => import('pages/Evaluator'))

export default function App(): ReactElement {
	return (
		<HashRouter>
			<Suspense fallback={<LoadingOrError />}>
				<Routes>
					<Route path='/' element={<Results />} />
					<Route path='/evaluators/:id' element={<Evaluator />} />
				</Routes>
			</Suspense>
		</HashRouter>
	)
}
