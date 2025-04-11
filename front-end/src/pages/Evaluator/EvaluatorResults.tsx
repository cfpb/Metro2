import { useQuery } from '@tanstack/react-query'
import { useNavigate, useSearch } from '@tanstack/react-router'
import Loader from 'components/Loader/Loader'
import type { EvaluatorHits } from 'models/EvaluatorHits'
import { evaluatorHitsQueryOptions } from 'models/EvaluatorHits'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import { useEffect } from 'react'
import type EvaluatorMetadata from './Evaluator'
import { getPageCount, getResultsMessage, getTableFields } from './EvaluatorUtils'
import EvaluatorFilterSidebar from './filters/FilterSidebar'

import EvaluatorDownloader from './EvaluatorDownloader'
import EvaluatorResultsPagination from './EvaluatorResultsPagination'
import EvaluatorTable from './EvaluatorTable'

interface EvaluatorTableData {
  evaluatorMetadata: EvaluatorMetadata
  eventData: Event
}

export default function EvaluatorResults({
  evaluatorMetadata,
  eventData
}: EvaluatorTableData): ReactElement {
  const navigate = useNavigate()

  const query = useSearch({ strict: false })
  const { page, view } = query
  const isFiltered = Object.keys(query).some(
    key => !['page', 'view', 'page_size'].includes(key)
  )

  // Fetch data from server
  const { data, isFetching } = useQuery<
    EvaluatorHits,
    Error,
    EvaluatorHits,
    string[]
  >(evaluatorHitsQueryOptions(String(eventData.id), evaluatorMetadata.id, query))

  const rows = data?.hits ?? []

  // Get list of fields to display for this evaluator
  const fields = getTableFields(
    evaluatorMetadata.fields_used ?? [],
    evaluatorMetadata.fields_display ?? []
  )

  const totalHits = evaluatorMetadata.hits
  const currentHits = data?.count ?? 0
  const pageCount = getPageCount(currentHits)

  // TODO: think about whether this is needed / when it should happen
  // should this be handled by the API?
  useEffect(() => {
    if (typeof page === 'number' && (page > pageCount || page <= 0)) {
      void navigate({
        to: '.',
        search: (prev: Record<string, unknown>) => ({ ...prev, page: 1 })
      })
    }
  })

  return (
    <div className='loader_wrapper'>
      {isFetching ? <Loader message='Your data is loading' /> : null}
      <div className='evaluator-hits-row'>
        <div className='row row__download '>
          <div data-testid='results-message'>
            <h4>
              {getResultsMessage(
                currentHits,
                totalHits,
                rows.length,
                view,
                isFiltered
              )}
            </h4>
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
            <div className='results_sidebar'>
              {view === 'all' ? <EvaluatorFilterSidebar /> : null}
            </div>
            <div className='results_table'>
              <EvaluatorTable data={rows} fields={fields} eventData={eventData} />
              {view === 'all' ? (
                <div className=''>
                  <EvaluatorResultsPagination pageCount={pageCount} page={page} />
                </div>
              ) : null}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
