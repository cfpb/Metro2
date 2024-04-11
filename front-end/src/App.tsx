import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { RouterProvider, createRouter } from '@tanstack/react-router'
import ErrorComponent from 'components/ErrorComponent'
import HeaderNavbar from 'components/HeaderNavbar'
import Loader from 'components/Loader/Loader'
import NotFound from 'components/NotFound'
import type { ReactElement } from 'react'
import './App.less'
import routeTree from './router'

// React-Query setup
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false
    }
  }
})

// Create a new router instance
const router = createRouter({
  routeTree,
  context: {
    queryClient
  },
  // delay before showing pending component
  defaultPendingMs: 0,
  defaultPendingComponent: Loader,
  defaultErrorComponent: ErrorComponent,
  defaultNotFoundComponent: NotFound,
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
      <header className='content-row'>
        <h1 className='h2 u-mb0'>Metro2 Evaluator Tool</h1>
      </header>
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </>
  )
}