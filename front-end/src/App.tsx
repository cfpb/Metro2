import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { RouterProvider, createRouter } from '@tanstack/react-router'
import ErrorComponent from 'components/Errors/ErrorComponent'
import NotFound from 'components/Errors/NotFound'
import Loader from 'components/Loader/Loader'
import WarningModal from 'components/Modals/WarningModal'
import { PageHeader } from 'design-system-react'
import type { ReactElement } from 'react'
import { stringifySearchParams } from 'utils/utils'
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
  stringifySearch: stringifySearchParams,
  getScrollRestorationKey: location => location.pathname
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
      <PageHeader href='/' />
      <WarningModal />
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </>
  )
}
