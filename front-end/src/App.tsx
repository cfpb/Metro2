import LoadingOrError from 'components/LoadingOrError'
import HeaderNavbar from 'components/HeaderNavbar'

import type { ReactElement } from 'react'
import { lazy, Suspense } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

import './App.less'

const HomePage = lazy(async () => import('pages/Home'))
const TestPage = lazy(async () => import('pages/Test'))

export default function App(): ReactElement {
	return (
		<>
			<HeaderNavbar />
			<div className='app'>
				<h1>Metro2 Evaluator Tool</h1>
				<BrowserRouter>
					<Suspense fallback={<LoadingOrError />}>
						<Routes>
							<Route path='/' element={<HomePage />} />
							<Route path='/test' element={<TestPage />} />
						</Routes>
					</Suspense>
				</BrowserRouter>
			</div>
		</>
	)
}
