import type EvaluatorMetadata from '../Evaluator/Evaluator'

export interface EventMetadata {
  id: number
  name: string
  description?: string
  start_date?: string
  end_date?: string
}

export default interface Event extends EventMetadata {
  evaluators: EvaluatorMetadata[]
}
