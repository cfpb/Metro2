import rootRoute from 'pages/rootRoute'
import indexRoute from 'pages/Landing/route'
import { eventRoute, eventIndexRoute } from 'pages/Event/route'
import evaluatorRoute from 'pages/Evaluator/route'
import accountRoute from 'pages/Account/route'

const routeTree = rootRoute.addChildren([
  eventRoute,
	eventIndexRoute,
	evaluatorRoute,
	accountRoute,
	indexRoute
])

export default routeTree
