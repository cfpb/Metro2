import rootRoute from 'pages/rootRoute'
import indexRoute from 'pages/Landing/route'
import { eventRoute, eventIndexRoute } from 'pages/Event/route'
import evaluatorRoute from 'pages/Evaluator/route'
import accountRoute from 'pages/Account/route'
import { guideRoute, overviewRoute, exploreRoute, contributeRoute, helpusRoute, adminRoute, tableRoute} from 'pages/Guide/route'

const routeTree = rootRoute.addChildren([
  eventRoute,
  eventIndexRoute,
  evaluatorRoute,
  accountRoute,
  guideRoute,
  indexRoute,
  overviewRoute,
  exploreRoute,
  tableRoute,
  contributeRoute,
  helpusRoute,
  adminRoute
])

export default routeTree
