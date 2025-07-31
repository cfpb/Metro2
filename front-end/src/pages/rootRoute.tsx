import type { QueryClient } from '@tanstack/react-query'
import { Link, Outlet, createRootRouteWithContext } from '@tanstack/react-router'
import LoadingOrError from 'components/LoadingOrError/LoadingOrError'
import type { ReactElement } from 'react'
import { Suspense } from 'react'
// import { TanStackRouterDevtools } from '@tanstack/router-devtools'

interface RouterContext {
  queryClient: QueryClient
}

const rootRoute = createRootRouteWithContext<RouterContext>()({
  component: (): ReactElement => (
    <Suspense fallback={<LoadingOrError />}>
      <header className='row row__action'>
        <h1 className='h4'>
          <Link to='/'>Metro2 Evaluator Tool</Link>
        </h1>
        <div className='links'>
          <Link to='/guide' className='nav-item'>
            Need help? See the user guide
          </Link>
        </div>
      </header>
      <div className='loader_wrapper'>
        <Outlet />
      </div>
      {/* <TanStackRouterDevtools /> */}
    </Suspense>
  )
})

export default rootRoute
