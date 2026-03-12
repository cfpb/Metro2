import type { QueryClient } from '@tanstack/react-query'
import { Link, Outlet, createRootRouteWithContext } from '@tanstack/react-router'
import LoadingOrError from 'components/LoadingOrError/LoadingOrError'
import { Suspense } from 'react'

interface RouterContext {
  queryClient: QueryClient
}

const rootRoute = createRootRouteWithContext<RouterContext>()({
  component: (): React.JSX.Element => (
    <Suspense fallback={<LoadingOrError />}>
      <header className='row row--action'>
        <h1 className='h4'>
          <Link to='/' className='a-link'>
            Metro2 Evaluator Tool
          </Link>
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
