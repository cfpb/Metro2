import type { QueryClient } from '@tanstack/react-query'
import type { ReactElement } from 'react'

import { Outlet, createRootRouteWithContext } from '@tanstack/react-router'
import { Suspense } from 'react'
import LoadingOrError from '../components/LoadingOrError'
// import { TanStackRouterDevtools } from '@tanstack/router-devtools'

interface RouterContext {
  queryClient: QueryClient
}

const rootRoute = createRootRouteWithContext<RouterContext>()({
  component: (): ReactElement => (
    <Suspense fallback={<LoadingOrError />}>
      <Outlet />
      {/* <TanStackRouterDevtools /> */}
    </Suspense>
  )
})

export default rootRoute
