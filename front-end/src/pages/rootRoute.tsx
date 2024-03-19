import type { ReactElement } from 'react'
import { Suspense } from 'react'
import { createRootRoute, Outlet } from '@tanstack/react-router'
// import { TanStackRouterDevtools } from '@tanstack/router-devtools'
import LoadingOrError from '../components/LoadingOrError'
import NotFound from 'components/NotFound'

const rootRoute = createRootRoute({
  component: (): ReactElement => (
      <Suspense fallback={ <LoadingOrError /> }>
        <Outlet />
        {/* <TanStackRouterDevtools /> */}
      </Suspense>
    ),
    notFoundComponent: NotFound
})

export default rootRoute
