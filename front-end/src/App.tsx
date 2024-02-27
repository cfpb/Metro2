import type { ReactElement } from 'react'
import { RouterProvider, createRouter } from '@tanstack/react-router'
import routeTree from './router'
import HeaderNavbar from 'components/HeaderNavbar'
import './App.less'

// Create a new router instance
const router = createRouter({ 
	routeTree
})

// Register the router instance for type safety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}

export default function App(): ReactElement {
	return (
		<>
		<HeaderNavbar />
		<header className="content-row">
			<h1 className="h2 u-mb0">Metro2 Evaluator Tool</h1>
		</header>
		<RouterProvider router={ router }/>
		</>
	)
}