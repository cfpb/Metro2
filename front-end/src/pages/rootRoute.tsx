import type { ReactElement } from 'react'
import { Suspense } from 'react'
import { createRootRoute, Outlet } from '@tanstack/react-router'
// import { TanStackRouterDevtools } from '@tanstack/router-devtools'
import LoadingOrError from '../components/LoadingOrError'

const rootRoute = createRootRoute({
  component: (): ReactElement => (
      <Suspense fallback={ <LoadingOrError /> }>
        <Outlet />
      </Suspense>
    )
})

export default rootRoute
