import Modal from 'components/DownloadModal'
import { Button } from 'design-system-react'
import type { ReactElement } from 'react'
import { useState } from 'react'
import type { AccountRecord, M2_FIELDS } from 'utils/constants'
import { downloadData, generateDownloadData } from 'utils/utils'

interface EvaluatorDownloadInterface {
  rows: AccountRecord[]
  fields: (typeof M2_FIELDS)[number][]
}

export default function EvaluatorDownloader({
  rows,
  fields
}: EvaluatorDownloadInterface): ReactElement {
  const [isOpen, setIsOpen] = useState(false)

  const onClose = (): void => {
    setIsOpen(false)
  }

  const onClick = (): void => {
    setIsOpen(true)
  }

  const onDownload = async (): Promise<void> => {
    const csv = generateDownloadData<AccountRecord>(fields, rows)
    try {
      await downloadData(csv, 'evaluator.csv')
      setIsOpen(false)
    } catch {
      // TODO determine if we need to handle errors
      setIsOpen(false)
    }
  }

  return (
    <div className='downloader'>
      <Button
        appearance='primary'
        label='Download evaluator results'
        iconRight='download'
        onClick={onClick}
        size='default'
      />
      <Modal open={isOpen} onClose={onClose} onDownload={onDownload} />
      <div id='portal' />
    </div>
  )
}
