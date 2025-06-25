import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import {
  Outlet,
  RouterProvider,
  createMemoryHistory,
  createRootRoute,
  createRoute,
  createRouter
} from '@tanstack/react-router'
import { mount } from 'cypress/react'
import type { ReactNode } from 'react'
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false
    }
  }
})

export const MountWithProviders = (component: ReactNode, options = {}) => {
  const rootRoute = createRootRoute({ component: Outlet })
  const indexRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: '/',
    component: () => component
  })
  const routeTree = rootRoute.addChildren([indexRoute])

  // Instantiate the router
  const router = createRouter({
    routeTree,
    context: {
      queryClient
    },
    history: createMemoryHistory({ initialEntries: ['/'] }), // Start at the root route
    defaultPendingMinMs: 0
  })

  mount(
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router as any} />
    </QueryClientProvider>
  )
}
