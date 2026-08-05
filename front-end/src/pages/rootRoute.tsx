import { DSRContext } from '@cfpb/design-system-react'
import { M2Footer } from '@src/components/Footer/Metro2Footer'
import { M2Header } from '@src/components/Header/Metro2Header'
import type { QueryClient } from '@tanstack/react-query'
import {
  createRootRouteWithContext,
  Outlet,
  Link as TanstackLink
} from '@tanstack/react-router'
import LoadingOrError from 'components/LoadingOrError/LoadingOrError'
import { Suspense } from 'react'
interface RouterContext {
  queryClient: QueryClient
}

const rootRoute = createRootRouteWithContext<RouterContext>()({
  component: (): React.JSX.Element => (
    <DSRContext value={{ LinkComponent: TanstackLink }}>
      <Suspense fallback={<LoadingOrError />}>
        {M2Header}
        <div className='app-container'>
          <Outlet />
        </div>
        {M2Footer}
        {/* <TanStackRouterDevtools /> */}
      </Suspense>
    </DSRContext>
  )
})

export default rootRoute
