import { PageHeader } from '@cfpb/design-system-react'
import { Link } from '@src/utils/DSRLink'
import type { QueryClient } from '@tanstack/react-query'
import { Outlet, createRootRouteWithContext } from '@tanstack/react-router'
import LoadingOrError from 'components/LoadingOrError/LoadingOrError'
import { Suspense } from 'react'

interface RouterContext {
  queryClient: QueryClient
}

const showCFPBHeader = import.meta.env.VITE_SHOW_CFPB_HEADER

const rootRoute = createRootRouteWithContext<RouterContext>()({
  component: (): React.JSX.Element => (
    <Suspense fallback={<LoadingOrError />}>
      {showCFPBHeader === 'true' ? (
        <PageHeader
          href='/'
          links={[
            <Link key='guide' to='/guide'>
              User guide
            </Link>
          ]}
        />
      ) : (
        <header className='row row--action' data-testid='metro2-header'>
          <h1 className='h4 u-mb0'>
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
      )}
      <div className='loader_wrapper'>
        <Outlet />
      </div>
      {/* <TanStackRouterDevtools /> */}
    </Suspense>
  )
})

export default rootRoute
