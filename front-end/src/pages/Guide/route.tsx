import { createRoute } from '@tanstack/react-router'
import rootRoute from '../rootRoute'
import GuidePage from './GuidePage'
import Overview from './Overview'
import Explore from './Explore'
import Contribute from './Contribute'
import HelpUs from './HelpUs'
import Admin from './Admin'

export const guideRoute = createRoute({
  path: '/guide',
  getParentRoute: () => rootRoute,
  component:GuidePage
})

export const overviewRoute = createRoute({
  path: '/',
  getParentRoute: () => guideRoute,
  component:Overview
})

export const exploreRoute = createRoute({
  path: '/explore',
  getParentRoute: () => guideRoute,
  component:Explore
})

export const contributeRoute = createRoute({
  path: '/contribute',
  getParentRoute: () => guideRoute,
  component:Contribute
})

export const helpusRoute = createRoute({
  path: '/help-us',
  getParentRoute: () => guideRoute,
  component:HelpUs
})

export const adminRoute = createRoute({
  path: '/m2admin',
  getParentRoute: () => guideRoute,
  component:Admin
})

export default guideRoute
