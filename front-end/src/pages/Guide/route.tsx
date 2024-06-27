import { createRoute } from '@tanstack/react-router'
import rootRoute from '../rootRoute'
import GuidePage from './GuidePage'

export const guideRoute = createRoute({
  path: '/guide',
  getParentRoute: () => rootRoute,
  component:GuidePage
})

export default guideRoute
