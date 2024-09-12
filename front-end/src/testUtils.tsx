/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import {
  Outlet,
  RouterProvider,
  createRootRoute,
  createRoute,
  createRouter
} from '@tanstack/react-router'
import { render } from '@testing-library/react'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false
    }
  }
})

export const DESKTOP_RESOLUTION_WIDTH = 1280
export const DESKTOP_RESOLUTION_HEIGHT = 800

export const MOBILE_RESOLUTION_WIDTH = 414
export const MOBILE_RESOLUTION_HEIGHT = 896

export default function renderWithProviders(component: React.JSX.Element): void {
  const rootRoute = createRootRoute({
    component: Outlet
  })

  const indexRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: '/',
    component: () => component
  })

  const routeTree = rootRoute.addChildren([indexRoute])
  const router = createRouter({
    routeTree,
    context: {
      queryClient
    }
  })

  render(
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router as any} />
    </QueryClientProvider>
  )
}
