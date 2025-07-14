import M2_FIELD_NAMES from '@src/constants/m2FieldNames'
import CopyUrl from 'components/CopyUrl'
import DownloadModal from 'components/Modals/DownloadModal'
import { Button } from 'design-system-react'
import { useEvaluatorResults } from 'queries/evaluatorHits'
import type { ReactElement } from 'react'
import { useState } from 'react'
import type AccountRecord from 'types/AccountRecord'
import type Event from 'types/Event'
import {
  downloadData,
  downloadFileFromURL,
  generateDownloadData
} from 'utils/downloads'
import { formatNumber } from 'utils/formatNumbers'

interface EvaluatorDownloadInterface {
  rows: AccountRecord[]
  fields: string[]
  evaluatorId: string
  eventData: Event
  view: 'all' | 'sample'
  isFiltered: boolean
  totalHits: number
  currentHits: number
  query: object
}

export default function EvaluatorDownloader({
  rows,
  fields,
  evaluatorId,
  eventData,
  view,
  isFiltered = false,
  totalHits,
  currentHits,
  query
}: EvaluatorDownloadInterface): ReactElement {
  const [isOpen, setIsOpen] = useState(false)

  /**
   * In case the user has applied filters and there are more results than are
   * currently shown in the table, we set up a request for *all* the results
   * for the current search params -- but cap it at 1 million because that's the
   * max number of rows Excel can display.
   *
   * We set the enabled option to false to prevent immediate request for this data.
   * We'll call refetch to initiate the actual fetch if / when the user
   * opts to download filtered results.
   */
  const { refetch } = useEvaluatorResults(
    eventData.id,
    evaluatorId,
    {
      ...query,
      page_size: currentHits > 1_000_000 ? 1_000_000 : currentHits
    },
    { enabled: false }
  )

  const onClose = (): void => {
    setIsOpen(false)
  }

  const onClick = (): void => {
    setIsOpen(true)
  }

  const onDownload = async (): Promise<void> => {
    if (!isFiltered && (view === 'all' || totalHits <= 20)) {
      /**
       * If you're viewing all the results (either because you're on the
       * all results view and no filters were applied or because you're on the
       * sample view but there are too few results for there to be a sample),
       * download the pre-generated full results file
       */
      const url = `/api/events/${eventData.id}/evaluator/${evaluatorId}/csv/`
      downloadFileFromURL(url)
      setIsOpen(false)
    } else {
      let csv
      if (view === 'all' && currentHits > rows.length) {
        /**
         * You've applied filters and aren't viewing all the filtered results,
         * so we get the rest of the filtered results and prep them for download
         */
        const result = await refetch()
        csv = generateDownloadData<AccountRecord>(
          fields,
          result.data?.hits ?? [],
          M2_FIELD_NAMES
        )
      } else {
        /**
         *  For all other cases, the results to download are already
         *  displayed in the table, so prep that data for download
         */
        csv = generateDownloadData<AccountRecord>(fields, rows, M2_FIELD_NAMES)
      }
      // Try downloading the data
      try {
        downloadData(
          csv,
          `${eventData.name}_${evaluatorId}_${
            view === 'all' ? 'filtered' : 'sample'
          }.csv`
        )

        setIsOpen(false)
      } catch {
        // TODO determine if we need to handle errors
        setIsOpen(false)
      }
    }
  }

  const modalContent = (
    <fieldset className='o-form_fieldset block block__sub'>
      <legend className='h4'>Save a link for later</legend>
      <p>
        Copy the link to this evaluator’s results. Any filters you’ve applied will be
        included.
      </p>
      <CopyUrl />
    </fieldset>
  )

  const resultsMessage =
    view === 'sample' && totalHits > 20
      ? 'Download representative sample of results'
      : `Download ${isFiltered && view === 'all' ? 'filtered' : 'all'} results`

  const buttonText =
    view === 'sample' && totalHits > 20
      ? 'Download 20 sample results'
      : `Download ${formatNumber(currentHits)} results`

  return (
    <div className='downloader'>
      <Button
        appearance='primary'
        label='Save results'
        iconRight='download'
        onClick={onClick}
        size='default'
      />
      <DownloadModal
        open={isOpen}
        onClose={onClose}
        onDownload={onDownload}
        content={modalContent}
        title='Save results'
        privacyAuthorizationHeader={resultsMessage}
        buttonText={buttonText}
      />
    </div>
  )
}
