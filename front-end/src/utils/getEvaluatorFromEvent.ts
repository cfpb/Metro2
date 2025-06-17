import type EvaluatorMetadata from 'types/EvaluatorMetadata'
import type Event from 'types/Event'

/**
 * getEvaluatorFromEvent()
 *
 * The data returned from the event API endpoint includes a list of the
 * evaluators that hit on the event, along with their stats for this event
 * (number of hits, number of accounts affected, etc)
 * and their basic metadata (category, description, etc).
 *
 * Instead of requesting information about an evaluator from a separate
 * endpoint when it's needed in the app, we retrieve it from the event object
 * which is always available on child pages under the event.
 *
 * @param {object} data - an Event object
 * @param {string} evaluatorId - id of an evaluator
 * @returns {object | undefined} evaluator's metadata or undefined
 */
const getEvaluatorDataFromEvent = (
  data: Event,
  evaluatorId: string
): EvaluatorMetadata | undefined =>
  data.evaluators.find((item: EvaluatorMetadata) => item.id === evaluatorId)

export default getEvaluatorDataFromEvent
