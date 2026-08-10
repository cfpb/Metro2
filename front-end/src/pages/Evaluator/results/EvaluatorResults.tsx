import { Icon, TabPanel } from '@cfpb/design-system-react'
import Loader from '@src/components/Loader/Loader'
import { ITEMS_PER_PAGE } from '@src/constants/settings'
import { useEvaluatorResults } from '@src/queries/evaluatorHits'
import type EvaluatorMetadata from '@src/types/EvaluatorMetadata'
import type Event from '@src/types/Event'
import { Link, useNavigate, useSearch } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import EvaluatorFilterSidebar from '../filters/FilterSidebar'
import type { EvaluatorSearch } from '../utils/evaluatorSearchSchema'
import './EvaluatorResults.scss'
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

  const query: EvaluatorSearch = useSearch({ strict: false })

  const { page, view, page_size, ...others } = query

  if (view == 'sample' && page != 1) {
    void navigate({
      to: '.',
      search: (prev: Record<string, unknown>) => ({ ...prev, page: 1 })
    })
  }

  // Fetch data from server
  const { data, isLoadingError, isFetching } = useEvaluatorResults(
    eventData.id,
    evaluatorMetadata.id,
    query
  )

  // Check if the search params include any of the filterable fields
  const isFiltered = Object.keys(others).some(key => filterableFields.includes(key))

  const rows = data?.hits ?? []

  // Get list of fields to display for this evaluator
  const fields = getTableFields(
    evaluatorMetadata.fields_used ?? [],
    evaluatorMetadata.fields_display ?? []
  )

  const totalHits = evaluatorMetadata.hits
  const currentHits =
    view === 'sample' ? (data?.hits.length ?? 0) : (data?.count ?? 0)

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
      <div className='row row--action u-mb0'>
        <EvaluatorResultsTabbedNavigation />
        <Link to='/guide/table' target='_blank'>
          See advanced table features
        </Link>
      </div>
      <div className='evaluator-hits-row'>
        <div className='loader__wrapper'>
          {isFetching ? <Loader message='Your data is loading' /> : null}
          <div className='row row--content u-mt0 u-mb0'>
            <TabPanel id={`${view === 'all' ? 'all' : 'sample'}`}>
              <div className={`results-container results-container--${view}`}>
                <div className='row row--action row--background'>
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
                          className='a-btn a-btn--link a-btn--warning'
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
                  <div className='results__sidebar sidebar'>
                    {view === 'all' ? <EvaluatorFilterSidebar /> : null}
                  </div>
                  <div className='results__table'>
                    <EvaluatorResultsTable
                      data={rows}
                      fields={fields}
                      eventData={eventData}
                      isLoading={isFetching}
                      isLoadingError={isLoadingError}
                    />
                    {view === 'all' && currentHits > 0 ? (
                      <div className='results__pagination'>
                        <EvaluatorResultsPagination
                          pageCount={pageCount}
                          page={currentHits === 0 ? 0 : page}
                        />
                      </div>
                    ) : null}
                  </div>
                </div>
              </div>
            </TabPanel>
          </div>
        </div>
      </div>
    </>
  )
}
