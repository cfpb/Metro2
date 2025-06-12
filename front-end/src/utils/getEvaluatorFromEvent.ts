import type EvaluatorMetadata from 'types/EvaluatorMetadata'
import type Event from 'types/Event'

const getEvaluatorDataFromEvent = (
  data: Event,
  evaluatorId: string
): EvaluatorMetadata | undefined =>
  data.evaluators.find((item: EvaluatorMetadata) => item.id === evaluatorId)

export default getEvaluatorDataFromEvent
