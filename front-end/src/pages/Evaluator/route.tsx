import { createRoute } from '@tanstack/react-router'
import { eventRoute } from '../Event/route'
import EvaluatorPage from './EvaluatorPage'

const evaluatorRoute = createRoute({
  path: '/evaluators/$evaluatorId',
  getParentRoute: () => eventRoute,
  component: EvaluatorPage
})

export default evaluatorRoute
