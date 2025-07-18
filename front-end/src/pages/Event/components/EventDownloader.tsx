import { Button } from 'design-system-react'
import { useState } from 'react'
import type { ReactElement } from 'react'
import type EvaluatorMetadata from 'types/EvaluatorMetadata'
import { downloadData, generateDownloadData } from 'utils/downloads'
import CopyUrl from 'components/CopyUrl'
import DownloadModal from '@src/components/Modals/DownloadModal'

interface EventDownloaderProperties {
  rows: EvaluatorMetadata[]
  eventName: string
}

export default function EventDownloader({
  rows,
  eventName
}: EventDownloaderProperties): ReactElement {
  const fields = ['id', 'description', 'category', 'hits', 'accounts_affected']
  const headerMap = new Map([
    ['id', 'ID'],
    ['description', 'DESCRIPTION'],
    ['category', 'CATEGORY'],
    ['hits', 'HITS'],
    ['accounts_affected', 'ACCOUNTS AFFECTED']
  ])

  const [isOpen, setIsOpen] = useState(false)
  
  const onClose = (): void => {
    setIsOpen(false)
  }

  const onClick = (): void => {
    setIsOpen(true)
  }

  const onDownload = async (): Promise<void> => {
    const csv = generateDownloadData(fields, rows, headerMap)
    const fileName = `${eventName}.csv`
    // eslint-disable-next-line @typescript-eslint/no-floating-promises
    downloadData(csv, fileName)
  }

    const copy = (
      <>
        <fieldset className='o-form_fieldset block block__sub'>
          <h3 className='h4'>Save a link for later</h3>
          <p>Copy the link to this event&apos;s results.</p>
          <CopyUrl/>
        </fieldset>

          <h3 className='h4'>Download a summary</h3>
          <p>            
            Choosing to download will create a .csv containing the results in the table only.
          </p>
      </>
    )
  
    return (
      <div className='downloader'>
        <Button
          appearance='primary'
          label='Save summary'
          iconRight='download'
          onClick={onClick}
          size='default'
        />
        <div id='portal' />
        <DownloadModal
          open={isOpen}
          onClose={onClose}
          onDownload={onDownload}
          content={copy}
          title='Save summary'
          buttonText = 'Download summary'
          hidePII
        />
      </div>
    )
}
