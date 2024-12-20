import type { QueryClient } from '@tanstack/react-query'
import { Link, Outlet, createRootRouteWithContext } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import { Suspense } from 'react'
import LoadingOrError from '../components/LoadingOrError'
// import { TanStackRouterDevtools } from '@tanstack/router-devtools'

interface RouterContext {
  queryClient: QueryClient
}

const rootRoute = createRootRouteWithContext<RouterContext>()({
  component: (): ReactElement => (
    <Suspense fallback={<LoadingOrError />}>
      <header className='content-row m2-nav'>
        <div className='navbar'>
          <h1 className='h4'>
            <Link to='/'>Metro2 Evaluator Tool</Link>
          </h1>
          <div className='nav-items'>
            <div className='links'>
             {<Link to='/guide' className='nav-item'>User guide</Link>}
            </div>
          </div>
        </div>
      </header>
      <Outlet />
      {/* <TanStackRouterDevtools /> */}
    </Suspense>
  )
})

export default rootRoute
