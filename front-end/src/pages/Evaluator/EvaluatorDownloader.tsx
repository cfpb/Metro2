import Modal from 'components/DownloadModal'
import { Button, RadioButton } from 'design-system-react'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import { useRef, useState } from 'react'
import type { AccountRecord, M2_FIELDS } from 'utils/constants'
import { FIELD_NAMES_LOOKUP } from 'utils/constants'
import { downloadData, downloadFileFromURL, generateDownloadData } from 'utils/utils'

interface EvaluatorDownloadInterface {
  rows: AccountRecord[]
  fields: (typeof M2_FIELDS)[number][]
  evaluatorId: string
  eventData: Event
}

export default function EvaluatorDownloader({
  rows,
  fields,
  evaluatorId,
  eventData
}: EvaluatorDownloadInterface): ReactElement {
  const [isOpen, setIsOpen] = useState(false)

  const allResults = useRef<HTMLInputElement>(null)

  const onClose = (): void => {
    setIsOpen(false)
  }

  const onClick = (): void => {
    setIsOpen(true)
  }

  const onDownload = async (): Promise<void> => {
    if (allResults.current?.checked) {
      const url = `/api/events/${eventData.id}/evaluator/${evaluatorId}/csv/`
      // await writeURLToFile('all_evaluator_results.csv', url)
      downloadFileFromURL(url)
      setIsOpen(false)
    } else {
      const csv = generateDownloadData<AccountRecord>(
        fields,
        rows,
        FIELD_NAMES_LOOKUP
      )
      try {
        await downloadData(csv, `${eventData.name}_${evaluatorId}_sample`)
        setIsOpen(false)
      } catch {
        // TODO determine if we need to handle errors
        setIsOpen(false)
      }
    }
  }

  const header = (
    <>
      <p>
        <b>Note: </b>
        {`Choosing "Save file" will create a file containing only the
        results in the table by default.`}
      </p>
      <div className='u-mb15 u-mt15'>
        <fieldset className='o-form_fieldset'>
          <legend className='h2'>Choose .csv options:</legend>
          <RadioButton
            id='sample'
            name='evaluator-download'
            label='Create a .csv with only the 20 results in the table'
            labelClassName=''
            labelInline
          />
          <RadioButton
            id='all'
            name='evaluator-download'
            label="Create a .csv containing all of this evaluator's results"
            labelClassName=''
            labelInline
            defaultChecked
            inputRef={allResults}
          />
        </fieldset>
      </div>
    </>
  )

  return (
    <div className='downloader'>
      <Button
        appearance='primary'
        label='Download evaluator results'
        iconRight='download'
        onClick={onClick}
        size='default'
      />
      <Modal
        open={isOpen}
        onClose={onClose}
        onDownload={onDownload}
        header={header}
      />
      <div id='portal' />
    </div>
  )
}
