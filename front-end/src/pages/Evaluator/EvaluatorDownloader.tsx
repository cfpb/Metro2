import { useQuery } from '@tanstack/react-query'
import CopyUrl from 'components/CopyUrl'
import DownloadModal from 'components/Modals/DownloadModal'
import { Button } from 'design-system-react'
import type { EvaluatorHits } from 'models/EvaluatorHits'
import { evaluatorHitsQueryOptions } from 'models/EvaluatorHits'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import { useState } from 'react'
import type { AccountRecord } from 'utils/constants'
import { M2_FIELD_NAMES } from 'utils/constants'
import { downloadData, downloadFileFromURL, generateDownloadData } from 'utils/utils'

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
   * Use {enabled: false} option to prevent immediate request for this data.
   * We'll call refetch to initiate the actual fetch if / when the user
   * opts to download filtered results.
   */
  const { data, refetch } = useQuery<EvaluatorHits, Error, EvaluatorHits, string[]>(
    evaluatorHitsQueryOptions(
      String(eventData.id),
      evaluatorId,
      {
        ...query,
        page_size: currentHits > 1_000_000 ? 1_000_000 : currentHits
      },
      { enabled: false }
    )
  )

  const onClose = (): void => {
    setIsOpen(false)
  }

  const onClick = (): void => {
    setIsOpen(true)
  }

  const onDownload = async (): Promise<void> => {
    if (view === 'all' && !isFiltered) {
      // If you're viewing all results and haven't applied filters,
      // download the pre-generated full results file
      const url = `/api/events/${eventData.id}/evaluator/${evaluatorId}/csv/`
      downloadFileFromURL(url)
      setIsOpen(false)
    } else {
      const ext = view === 'all' ? 'filtered' : 'sample'
      let csv
      // If you've applied filters and aren't viewing all the filtered results,
      // get the rest of the filtered results and prep them for download
      if (view === 'all' && isFiltered && currentHits > rows.length) {
        const result = await refetch()
        csv = generateDownloadData<AccountRecord>(
          fields,
          result.data?.hits ?? [],
          M2_FIELD_NAMES
        )
      } else {
        // For all other cases, the results to download are already
        // displayed in the table, so prep that data for download

        // TODO: if there are fewer than 20 results for this evaluator,
        // downloading with results toggle set to 'sample' will give you a front-end
        // generated file with annotations but downloading from the 'all'
        // view will get you the pre-generated results file without annotations.
        // Maybe there should only be a single all results view when there's no sample?
        csv = generateDownloadData<AccountRecord>(fields, rows, M2_FIELD_NAMES)
      }
      // Try downloading the data
      try {
        await downloadData(csv, `${eventData.name}_${evaluatorId}_${ext}`)
        setIsOpen(false)
      } catch {
        // TODO determine if we need to handle errors
        setIsOpen(false)
      }
    }
  }

  let resultsMessage = 'all results for this evaluator'
  if (view === 'sample' && totalHits > 20)
    resultsMessage = 'a representative sample of results for this evaluator'
  if (view === 'all' && isFiltered)
    resultsMessage = 'results for the currently applied filters'

  const header = (
    <>
      <fieldset className='o-form_fieldset block block__sub'>
        <legend className='h4'>Save a link to these results</legend>
        <CopyUrl url='' />
      </fieldset>
      <legend className='h4'>Download {resultsMessage}</legend>
    </>
  )

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
        header={header}
        title='Save results'
      />
    </div>
  )
}
