import { createRoute } from '@tanstack/react-router'
import rootRoute from '../rootRoute'
import Admin from './Admin'
import Contribute from './Contribute'
import Explore from './Explore'
import GuidePage from './GuidePage'
import HelpUs from './HelpUs'
import Overview from './Overview'
import Table from './Table'

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
