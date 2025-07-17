import ErrorComponent from '@src/components/Error/ErrorComponent'
import NotFound from '@src/components/Error/NotFound'
import WarningModal from '@src/components/Modal/WarningModal'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import {
  RouterProvider,
  createRouter,
  parseSearchWith
} from '@tanstack/react-router'
import Loader from 'components/Loader/Loader'
import type { ReactElement } from 'react'

import customParser from 'utils/customParser'
import { stringifySearchParams } from 'utils/customStringify'
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
  parseSearch: parseSearchWith(customParser),
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
      <WarningModal />
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </>
  )
}
