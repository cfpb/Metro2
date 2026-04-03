import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import {
  RouterProvider,
  createRouter,
  parseSearchWith
} from '@tanstack/react-router'
import ErrorComponent from 'components/Error/ErrorComponent'
import NotFoundMessage from 'components/Error/NotFound'
import Loader from 'components/Loader/Loader'
import WarningModal from 'components/Modal/WarningModal'
import type { ReactElement } from 'react'

import customParser from 'utils/customParser'
import { stringifySearchParams } from 'utils/customStringify'
import './App.scss'
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
  stringifySearch: stringifySearchParams,
  parseSearch: parseSearchWith(customParser),
  getScrollRestorationKey: location => location.pathname,
  defaultNotFoundComponent: NotFoundMessage
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
      <WarningModal />
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </>
  )
}
