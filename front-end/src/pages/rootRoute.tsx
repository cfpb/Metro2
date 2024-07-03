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
      <header className='content-row m2-nav'>
        <div className='navbar'>
          <h2 className='h4 u-mb0'>
            <Link to='/'>Metro2 Evaluator Tool</Link>            
          </h2>
          <div className='nav-items'>
            <div className='links'>
             {/* <Link to='/guide' className='nav-item'>User guide</Link> */}
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
