import DownloadModal from 'components/Modals/DownloadModal'
import { Button, RadioButton } from 'design-system-react'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import { useRef, useState } from 'react'
import type { AccountRecord} from 'utils/constants';
import { M2_FIELD_NAMES } from 'utils/constants'
import { downloadData, downloadFileFromURL, generateDownloadData } from 'utils/utils'

interface EvaluatorDownloadInterface {
  rows: AccountRecord[]
  fields: string[]
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

  const header = (
    <fieldset className='o-form_fieldset block block__sub'>
      <legend className='h4'>Choose .csv options:</legend>
      <RadioButton
        id='sample'
        name='evaluator-download'
        label={`Create a .csv with only the ${rows.length} result${
          rows.length > 1 ? 's' : ''
        } in the table`}
        labelClassName=''
        labelInline
        defaultChecked
        isLarge
      />
      <RadioButton
        id='all'
        name='evaluator-download'
        label="Create a .csv containing all of this evaluator's results"
        labelClassName=''
        labelInline
        inputRef={allResults}
        isLarge
      />
    </fieldset>
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
      <DownloadModal
        open={isOpen}
        onClose={onClose}
        onDownload={onDownload}
        header={header}
      />
    </div>
  )
}
