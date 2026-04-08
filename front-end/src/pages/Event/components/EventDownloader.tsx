import { Button } from '@cfpb/design-system-react'
import DownloadModal from '@src/components/Modal/DownloadModal'
import type { ReactElement } from 'react'
import { useState } from 'react'
import type EvaluatorMetadata from 'types/EvaluatorMetadata'
import { downloadData, generateDownloadData } from 'utils/downloads'

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

  const onDownload = (): void => {
    const csv = generateDownloadData(fields, rows, headerMap)
    const fileName = `${eventName}.csv`
    try {
      downloadData(csv, fileName)
      setIsOpen(false)
    } catch {
      // TODO determine if we need to handle errors
      setIsOpen(false)
    }
  }

  const copy = (
    <>
      <h3 className='h4'>Download a summary</h3>
      <p>
        Choosing to download will create a .csv containing the results in the table
        only.
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
        data-testid='download-event-summary'
      />
      <div id='portal' />
      <DownloadModal
        open={isOpen}
        onClose={onClose}
        onDownload={onDownload}
        title='Save summary'
        copyText="Copy the link to this event's results"
        content={copy}
        requirePrivacyAcknowledgment={false}
        buttonText='Download summary'
      />
    </div>
  )
}
