import { createRoute } from '@tanstack/react-router'
import rootRoute from '../rootRoute'
import LandingPage from './LandingPage'

const indexRoute = createRoute( {
  path: '/',
  getParentRoute: () => rootRoute,
  component: LandingPage
} )

export default indexRoute