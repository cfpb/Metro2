import type EvaluatorMetadata from './EvaluatorMetadata'
import type EventMetadata from './EventMetadata'

export default interface Event extends EventMetadata {
  evaluators: EvaluatorMetadata[]
}
