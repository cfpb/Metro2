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
        <h2 className='h4 u-mb0 nav'>
          <Link to='/' className='nav-item'>Metro2 Evaluator Tool</Link>
          <Link to='/guide' className='nav-item'>User Guide</Link>
        </h2>
      </header>
      <Outlet />
      {/* <TanStackRouterDevtools /> */}
    </Suspense>
  )
})

export default rootRoute
