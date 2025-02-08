import { useQuery } from '@tanstack/react-query'
import { useNavigate, useSearch } from '@tanstack/react-router'
import Loader from 'components/Loader/Loader'
import { evaluatorHitsQueryOptions } from 'models/EvaluatorHits'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import { useEffect } from 'react'
import type { AccountRecord } from 'utils/constants'
import type EvaluatorMetadata from './Evaluator'
import EvaluatorDownloader from './EvaluatorDownloader'
import EvaluatorResultsPagination from './EvaluatorResultsPagination'
import EvaluatorTable from './EvaluatorTable'
import {
  getFieldsToDisplay,
  getPageCount,
  getResultsMessage
} from './EvaluatorUtils'

interface EvaluatorTableData {
  evaluatorMetadata: EvaluatorMetadata
  eventData: Event
}

export default function EvaluatorResults({
  evaluatorMetadata,
  eventData
}: EvaluatorTableData): ReactElement {
  const navigate = useNavigate()
  const query = useSearch({
    // from: '/events/$eventId/evaluators/$evaluatorId' as const
    strict: false
  })
  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
  const { page, view } = query
  // const page: number = typeof query.page === 'number' ? query.page : 1
  // // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
  // const view =
  //   query.view === 'all' || query.view === 'sample' ? query.view : 'sample'

  // Fetch data from server
  const { data, isFetching } = useQuery<
    AccountRecord[],
    Error,
    AccountRecord[],
    string[]
  >(evaluatorHitsQueryOptions(String(eventData.id), evaluatorMetadata.id, query))

  const rows = data ?? []

  // Get list of fields to display for this evaluator
  const fields = getFieldsToDisplay(
    evaluatorMetadata.fields_used ?? [],
    evaluatorMetadata.fields_display ?? []
  )

  const hitsCount = evaluatorMetadata.hits
  const pageCount = Math.ceil(hitsCount / 20)

  // TODO: think about whether this is needed / when it should happen
  // should this be handled by the API?
  useEffect(() => {
    if (typeof page === 'number' && (page > pageCount || page <= 0)) {
      void navigate({
        to: '.',
        search: prev => ({ ...prev, page: 1 })
      })
    }
  })

  return (
    <div className='loader_wrapper'>
      {isFetching ? <Loader message='Your data is loading' /> : null}
      <div className='evaluator-hits-row'>
        <div className='row row__download '>
          <div data-testid='results-message'>
            {/* eslint-disable-next-line @typescript-eslint/no-unsafe-argument */}
            <h4>{getResultsMessage(hitsCount, rows.length, view, page)}</h4>
          </div>
          <EvaluatorDownloader
            rows={rows}
            fields={fields}
            eventData={eventData}
            evaluatorId={evaluatorMetadata.id}
          />
        </div>
        <div className='row row__content '>
          <div className={`results results__${view} u-mb30`}>
            <div className='results_table'>
              <EvaluatorTable data={rows} fields={fields} eventData={eventData} />
              {view === 'all' ? (
                <div className=''>
                  <EvaluatorResultsPagination
                    pageCount={getPageCount(hitsCount)}
                    page={page}
                  />
                </div>
              ) : null}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
