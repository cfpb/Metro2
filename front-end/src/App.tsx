import LoadingOrError from 'components/LoadingOrError'
import HeaderNavbar from 'components/HeaderNavbar'

import type { ReactElement } from 'react'
import { lazy, Suspense } from 'react'
import { HashRouter, Route, Routes } from 'react-router-dom'

import './App.less'

const HomePage = lazy(async () => import('pages/Home'))

export default function App(): ReactElement {
	return (
		<>
			<HeaderNavbar />
			<div className='app'>
				<h1>Metro2 Evaluator Tool</h1>
				<HashRouter>
					<Suspense fallback={<LoadingOrError />}>
						<Routes>
							<Route path='/' element={<HomePage />} />
						</Routes>
					</Suspense>
				</HashRouter>
			</div>
		</>
	)
}
