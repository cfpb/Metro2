import DownloadModal from 'components/Modals/DownloadModal'
import { Button } from 'design-system-react'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import { useState } from 'react'
import type { AccountRecord, M2_FIELDS } from 'utils/constants'
import { FIELD_NAMES_LOOKUP } from 'utils/constants'
import { downloadData, generateDownloadData } from 'utils/utils'

interface AccountDownloadInterface {
  rows: AccountRecord[]
  fields: (typeof M2_FIELDS)[number][]
  accountId: string
  eventData: Event
}

export default function AccountDownloader({
  rows,
  fields,
  accountId,
  eventData
}: AccountDownloadInterface): ReactElement {
  const [isOpen, setIsOpen] = useState(false)

  const onClose = (): void => {
    setIsOpen(false)
  }

  const onClick = (): void => {
    setIsOpen(true)
  }

  const onDownload = async (): Promise<void> => {
    const csv = generateDownloadData<AccountRecord>(fields, rows, FIELD_NAMES_LOOKUP)
    try {
      await downloadData(csv, `${eventData.name}_${accountId}.csv`)
      setIsOpen(false)
    } catch {
      // TODO determine if we need to handle errors
      setIsOpen(false)
    }
  }

  const header = (
    <p>
      <b>Note: </b>Choosing to download a CSV will create a file that contains all
      data for account {accountId} for the given date range. This file will contain
      both PII and CI.
    </p>
  )

  return (
    <div className='downloader'>
      <Button
        appearance='primary'
        label='Download account data'
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
