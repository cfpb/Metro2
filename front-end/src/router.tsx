import {
  accountRoute,
  accountSearchRoute,
  accountsRoute
} from '@src/pages/Account/route'
import evaluatorRoute from '@src/pages/Evaluator/route'
import { eventIndexRoute, eventRoute } from '@src/pages/Event/route'
import {
  adminRoute,
  contributeRoute,
  exploreRoute,
  guideRoute,
  helpusRoute,
  overviewRoute,
  tableRoute
} from '@src/pages/Guide/route'
import indexRoute from '@src/pages/Landing/route'
import rootRoute from '@src/pages/rootRoute'

const routeTree = rootRoute.addChildren([
  indexRoute,
  eventRoute.addChildren([
    eventIndexRoute,
    evaluatorRoute,
    accountsRoute.addChildren([accountSearchRoute, accountRoute])
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
