import type { QueryClient } from '@tanstack/react-query'
import type { ReactElement } from 'react'

import { Link, Outlet, createRootRouteWithContext } from '@tanstack/react-router'
import { Suspense } from 'react'
import LoadingOrError from '../components/LoadingOrError'
// import { TanStackRouterDevtools } from '@tanstack/router-devtools'

interface RouterContext {
  queryClient: QueryClient
}

const rootRoute = createRootRouteWithContext<RouterContext>()({
  component: (): ReactElement => (
    <Suspense fallback={<LoadingOrError />}>
      <header className='content-row'>
        <h2 className='h4 u-mb0'>
          <Link to='/'>Metro2 Evaluator Tool</Link>
        </h2>
      </header>
      <Outlet />
      {/* <TanStackRouterDevtools /> */}
    </Suspense>
  )
})

export default rootRoute
