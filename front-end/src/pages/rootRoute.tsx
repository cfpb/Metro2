import {
  AppFooter,
  DSRContext,
  Link as DSRLink,
  Header,
  type LinkProperties
} from '@cfpb/design-system-react'
import type { QueryClient } from '@tanstack/react-query'
import {
  createRootRouteWithContext,
  Outlet,
  Link as TanstackLink
} from '@tanstack/react-router'
import LoadingOrError from 'components/LoadingOrError/LoadingOrError'
import DOMPurify from 'dompurify'
import { Suspense } from 'react'

interface RouterContext {
  queryClient: QueryClient
}

const showCFPBHeader = import.meta.env.VITE_SHOW_CFPB_HEADER
const footerContent = DOMPurify.sanitize(
  import.meta.env.VITE_FOOTER_CONTENT as string
)

const footerLinks = JSON.parse(import.meta.env.VITE_FOOTER_LINKS as string) as Omit<
  LinkProperties,
  'preload'
>[]

const rootRoute = createRootRouteWithContext<RouterContext>()({
  component: (): React.JSX.Element => (
    <DSRContext value={{ LinkComponent: TanstackLink }}>
      <Suspense fallback={<LoadingOrError />}>
        {showCFPBHeader === 'true' ? (
          <Header
            href='/'
            links={[
              <DSRLink key='guide' to='/guide'>
                User guide
              </DSRLink>
            ]}
          />
        ) : (
          <header className='row row--action' data-testid='metro2-header'>
            <h1 className='h4 u-mb0'>
              <DSRLink to='/' className='a-link'>
                Metro2 Evaluator Tool
              </DSRLink>
            </h1>
            <div className='links'>
              <DSRLink to='/guide' className='nav-item'>
                Need help? See the user guide
              </DSRLink>
            </div>
          </header>
        )}
        <div className='app-container'>
          <Outlet />
        </div>
        <AppFooter
          navLinks={footerLinks.map(link => {
            const { label, ...others } = link
            return <DSRLink key={label} label={label} {...others} />
          })}
          footerContent={
            <div
              data-testid='footer-content'
              dangerouslySetInnerHTML={{ __html: footerContent }}
            />
          }></AppFooter>
        {/* <TanStackRouterDevtools /> */}
      </Suspense>
    </DSRContext>
  )
})

export default rootRoute
