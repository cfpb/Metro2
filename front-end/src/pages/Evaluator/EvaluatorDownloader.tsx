import { useQuery } from '@tanstack/react-query'
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

  const { data, refetch } = useQuery<EvaluatorHits, Error, EvaluatorHits, string[]>(
    evaluatorHitsQueryOptions(String(eventData.id), evaluatorId, {
      ...query,
      download: 'all',
      page_size: currentHits
    })
  )

  const onClose = (): void => {
    setIsOpen(false)
  }

  const onClick = (): void => {
    setIsOpen(true)
  }

  const onDownload = async (): Promise<void> => {
    if (view === 'all') {
      if (isFiltered) {
        if (currentHits === rows.length) {
          // download what's in the table because that's all the filtered results
          const csv = generateDownloadData<AccountRecord>(
            fields,
            rows,
            M2_FIELD_NAMES
          )
          try {
            await downloadData(csv, `${eventData.name}_${evaluatorId}_filtered`)
            setIsOpen(false)
          } catch {
            // TODO determine if we need to handle errors
            setIsOpen(false)
          }
        } else {
          // there are more filtered results than what's in the table
          // get and download them all
          await refetch()
          const csv = generateDownloadData<AccountRecord>(
            fields,
            data.hits,
            M2_FIELD_NAMES
          )
          try {
            await downloadData(csv, `${eventData.name}_${evaluatorId}_filtered`)
            setIsOpen(false)
          } catch {
            // TODO determine if we need to handle errors
            setIsOpen(false)
          }
        }
      } else {
        const url = `/api/events/${eventData.id}/evaluator/${evaluatorId}/csv/`
        // await writeURLToFile('all_evaluator_results.csv', url)
        downloadFileFromURL(url)
        setIsOpen(false)
      }
    } else {
      const csv = generateDownloadData<AccountRecord>(fields, rows, M2_FIELD_NAMES)
      try {
        await downloadData(csv, `${eventData.name}_${evaluatorId}_sample`)
        setIsOpen(false)
      } catch {
        // TODO determine if we need to handle errors
        setIsOpen(false)
      }
    }
  }

  let message = ''
  if (view === 'all') {
    message = isFiltered
      ? 'all results for this evalutor with the filters you have applied'
      : 'all results for this evaluator'
  } else {
    message =
      totalHits > 20
        ? 'the representative sample of results for this evaluator'
        : 'all results for this evaluator'
  }
  const header = (
    <p>
      <b>Clicking the save button will download {message}</b>.
    </p>
    // <div className=' block block__sub'>{message}</div>
    // <fieldset className='o-form_fieldset block block__sub'>
    //   <legend className='h4'>Choose .csv options:</legend>
    //   <RadioButton
    //     id='sample'
    //     name='evaluator-download'
    //     label={`Create a .csv with only the ${rows.length} result${
    //       rows.length > 1 ? 's' : ''
    //     } in the table`}
    //     labelClassName=''
    //     labelInline
    //     defaultChecked
    //     isLarge
    //   />
    //   <RadioButton
    //     id='all'
    //     name='evaluator-download'
    //     label="Create a .csv containing all of this evaluator's results"
    //     labelClassName=''
    //     labelInline
    //     inputRef={allResults}
    //     isLarge
    //   />
    // </fieldset>
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
