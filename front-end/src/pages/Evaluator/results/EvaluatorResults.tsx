import { ITEMS_PER_PAGE } from '@src/constants/settings'
import { Link, useNavigate, useSearch } from '@tanstack/react-router'
import Loader from 'components/Loader/Loader'
import { Icon } from 'design-system-react'

import { useEvaluatorResults } from 'queries/evaluatorHits'
import type { ReactElement } from 'react'
import type EvaluatorMetadata from 'types/EvaluatorMetadata'
import type Event from 'types/Event'
import EvaluatorFilterSidebar from '../filters/EvaluatorFilterSidebar/FilterSidebar'
import './EvaluatorResults.less'
import EvaluatorDownloader from './components/Downloader'
import EvaluatorResultsMessage from './components/ResultsMessage'
import EvaluatorResultsPagination from './components/ResultsPagination'
import EvaluatorResultsTabbedNavigation from './components/ResultsTabbedNavigation'
import EvaluatorResultsTable from './components/ResultsTable'
import filterableFields from './utils/getFilterableFields'
import getPageCount from './utils/getPageCount'
import getTableFields from './utils/getTableFields'

interface EvaluatorResultsData {
  evaluatorMetadata: EvaluatorMetadata
  eventData: Event
}

export default function EvaluatorResults({
  evaluatorMetadata,
  eventData
}: EvaluatorResultsData): ReactElement {
  const navigate = useNavigate()

  const query = useSearch({ strict: false })
  // eslint-disable-next-line @typescript-eslint/naming-convention
  const { page, view, page_size } = query

  // Check if the search params include any of the filterable fields
  const isFiltered = Object.keys(query).some(key => filterableFields.includes(key))

  // Fetch data from server
  const { data, isLoadingError, isFetching } = useEvaluatorResults(
    eventData.id,
    evaluatorMetadata.id,
    query
  )

  const rows = data?.hits ?? []

  // Get list of fields to display for this evaluator
  const fields = getTableFields(
    evaluatorMetadata.fields_used ?? [],
    evaluatorMetadata.fields_display ?? []
  )

  const totalHits = evaluatorMetadata.hits
  const currentHits = data?.count ?? 0
  const pageCount = getPageCount(currentHits, page_size)

  // TODO: consider refining this to handle 404s for invalid page
  // differently than other misc errors
  if (isLoadingError && typeof page === 'number' && page > pageCount) {
    void navigate({
      to: '.',
      search: (prev: Record<string, unknown>) => ({ ...prev, page: 1 })
    })
  }

  return (
    <>
      <div className='row row__action u-mb0'>
        <EvaluatorResultsTabbedNavigation />
        <Link to='/guide/table' target='_blank'>
          See advanced table features
        </Link>
      </div>
      <div className='loader_wrapper'>
        {isFetching ? <Loader message='Your data is loading' /> : null}
        <div className='evaluator-hits-row'>
          <div className='row row__content u-mt0 tab-panel'>
            <div className='tab-panel'>
              <div className={`results-container results-container__${view}`}>
                <div className='row row__action '>
                  <div className='results-message' data-testid='results-message'>
                    <EvaluatorResultsMessage
                      page={page ?? 1}
                      view={view ?? 'sample'}
                      pageSize={page_size ?? ITEMS_PER_PAGE}
                      isFiltered={isFiltered}
                      currentHitsCount={currentHits}
                      totalResultsCount={totalHits}
                      isFetching={isFetching}
                    />
                    {isFiltered ? (
                      <p>
                        <Link
                          className='a-btn a-btn__link a-btn__warning'
                          to='.'
                          resetScroll={false}
                          search={(prev): object => ({
                            page: 1,
                            page_size: prev.page_size,
                            view: 'all'
                          })}
                          activeOptions={{ exact: true }}
                          style={{ pointerEvents: 'auto' }}
                          data-testid='remove-all-filters'>
                          <Icon name='error' />
                          Clear all filters
                        </Link>
                      </p>
                    ) : null}
                  </div>
                  <EvaluatorDownloader
                    rows={rows}
                    fields={fields}
                    eventData={eventData}
                    evaluatorId={evaluatorMetadata.id}
                    isFiltered={isFiltered}
                    view={view ?? 'sample'}
                    totalHits={totalHits}
                    currentHits={currentHits}
                    query={query}
                  />
                </div>
                <div className='results'>
                  <div className='results_sidebar sidebar'>
                    {view === 'all' ? <EvaluatorFilterSidebar /> : null}
                  </div>
                  <div className='results_table'>
                    <EvaluatorResultsTable
                      data={rows}
                      fields={fields}
                      eventData={eventData}
                      isLoading={isFetching}
                      isLoadingError={isLoadingError}
                    />
                    {view === 'all' && currentHits > 0 ? (
                      <div className='results_pagination'>
                        <EvaluatorResultsPagination
                          pageCount={pageCount}
                          page={currentHits === 0 ? 0 : page}
                        />
                      </div>
                    ) : null}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
