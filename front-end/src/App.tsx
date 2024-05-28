import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { RouterProvider, createRouter } from '@tanstack/react-router'
import ErrorComponent from 'components/Errors/ErrorComponent'
import NotFound from 'components/Errors/NotFound'
import Loader from 'components/Loader/Loader'
import { PageHeader } from 'design-system-react'
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
  defaultNotFoundComponent: NotFound
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
      <PageHeader />
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </>
  )
}
