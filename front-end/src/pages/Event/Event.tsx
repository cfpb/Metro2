import type EvaluatorMetadata from '../Evaluator/Evaluator'

export default interface Event {
  id: number
  name: string
  start_date: string
  end_date: string
  evaluators: EvaluatorMetadata[]
}
