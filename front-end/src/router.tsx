import accountRoute from 'pages/Account/route'
import evaluatorRoute from 'pages/Evaluator/route'
import { eventIndexRoute, eventRoute } from 'pages/Event/route'
import {
  adminRoute,
  contributeRoute,
  exploreRoute,
  guideRoute,
  helpusRoute,
  overviewRoute,
  tableRoute
} from 'pages/Guide/route'
import indexRoute from 'pages/Landing/route'
import rootRoute from 'pages/rootRoute'

const routeTree = rootRoute.addChildren([
  indexRoute,

  eventRoute.addChildren([
    eventIndexRoute,
    evaluatorRoute,
    accountRoute,
  ]),
  
  guideRoute,
  overviewRoute,
  exploreRoute,
  tableRoute,
  contributeRoute,
  helpusRoute,
  adminRoute
])

export default routeTree