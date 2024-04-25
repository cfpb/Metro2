import type { QueryClient } from '@tanstack/react-query'
import type { ReactElement } from 'react'

import { Outlet, createRootRouteWithContext, Link } from '@tanstack/react-router'
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
        <h1 className='h2 u-mb0'>
          <Link to='/'>Metro2 Evaluator Tool</Link>
        </h1>
      </header>
      <Outlet />
      {/* <TanStackRouterDevtools /> */}
    </Suspense>
  )
})

export default rootRoute
