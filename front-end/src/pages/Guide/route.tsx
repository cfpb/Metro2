import { createRoute } from '@tanstack/react-router'
import rootRoute from '../rootRoute'
import GuidePage from './GuidePage/GuidePage'
import Admin from './sections/Admin'
import Contribute from './sections/Contribute'
import Explore from './sections/Explore'
import HelpUs from './sections/HelpUs'
import Overview from './sections/Overview'
import Table from './sections/Table'

export const guideRoute = createRoute({
  path: '/guide',
  getParentRoute: () => rootRoute,
  component: GuidePage
})

export const overviewRoute = createRoute({
  path: '/',
  getParentRoute: () => guideRoute,
  component: Overview
})

export const exploreRoute = createRoute({
  path: '/explore',
  getParentRoute: () => guideRoute,
  component: Explore
})

export const tableRoute = createRoute({
  path: '/table',
  getParentRoute: () => guideRoute,
  component: Table
})

export const contributeRoute = createRoute({
  path: '/contribute',
  getParentRoute: () => guideRoute,
  component: Contribute
})

export const helpusRoute = createRoute({
  path: '/help-us',
  getParentRoute: () => guideRoute,
  component: HelpUs
})

export const adminRoute = createRoute({
  path: '/m2admin',
  getParentRoute: () => guideRoute,
  component: Admin
})

export default guideRoute
