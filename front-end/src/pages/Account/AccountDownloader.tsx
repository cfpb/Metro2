import { useQueryClient } from '@tanstack/react-query'
import DownloadModal from 'components/Modals/DownloadModal'
import { Button, RadioButton } from 'design-system-react'
import { Workbook } from 'exceljs'
import {
  ACCOUNT_HOLDER_FIELDS,
  accountHolderQueryOptions
} from 'models/AccountHolder'
import type Event from 'pages/Event/Event'
import { EVENT_FIELDS } from 'pages/Event/Event'
import type { ReactElement } from 'react'
import { useRef, useState } from 'react'
import type { AccountRecord } from 'utils/constants'
import { M2_FIELD_NAMES } from 'utils/constants'
import { getHeaderName } from 'utils/utils'

interface AccountDownloadInterface {
  rows: AccountRecord[]
  fields: string[]
  accountId: string
  eventData: Event
}
export default function AccountDownloader({
  rows,
  fields,
  accountId,
  eventData
}: AccountDownloadInterface): ReactElement {
  const queryClient = useQueryClient()

  const [isOpen, setIsOpen] = useState(false)

  const includeContactInfo = useRef<HTMLInputElement>(null)

  const onClose = (): void => {
    setIsOpen(false)
  }

  const onClick = (): void => {
    setIsOpen(true)
  }

  const onDownload = async (): Promise<void> => {
    // create a new Excel workbook
    const workbook = new Workbook()

    // create a sheet for the account records
    const accountRecordsSheet = workbook.addWorksheet('Account records', {
      views: [{ state: 'frozen', xSplit: 1, ySplit: 1 }]
    })
    // add columns for each account record field
    // 'fields' is a subset of M2_FIELD_NAMES, excluding 'cons_acct_num'
    accountRecordsSheet.columns = fields.map(field => ({
      key: field,
      header: getHeaderName(field, M2_FIELD_NAMES)
    }))
    // create a row in the sheet for each record
    accountRecordsSheet.addRows(rows)

    // include account holder contact info only if user has selected that option
    if (includeContactInfo.current?.checked) {
      // add a sheet for the account holder data
      const accountHolderSheet = workbook.addWorksheet('Account holder information')
      // get account holder data
      const data = await queryClient.fetchQuery(
        accountHolderQueryOptions(eventData.id, accountId)
      )
      // add columns for each of the account holder fields
      accountHolderSheet.columns = Array.from(
        ACCOUNT_HOLDER_FIELDS,
        ([key, header]) => ({ key, header })
      )
      // add a row with the account holder data
      accountHolderSheet.addRow(data)
    }

    // Add a sheet for event data
    const eventSheet = workbook.addWorksheet('Event information')
    // add columns for each of the event fields
    eventSheet.columns = Array.from(EVENT_FIELDS, ([key, header]) => ({
      key,
      header
    }))
    // add a row with the event holder data
    eventSheet.addRow(eventData)

    const buffer = await workbook.xlsx.writeBuffer()
    try {
      const handle = await showSaveFilePicker({
        suggestedName: `${eventData.name}_${accountId}.xlsx`,
        // @ts-expect-error Typescript doesn't handle File System API well
        startIn: 'downloads',
        types: [
          {
            description: 'Excel',
            accept: {
              'text/xlsx': ['.xlsx']
            }
          }
        ]
      })
      const writable = await handle.createWritable()
      // eslint-disable-next-line @typescript-eslint/no-floating-promises
      await writable.write(buffer)
      // eslint-disable-next-line @typescript-eslint/no-floating-promises
      writable.close()
      setIsOpen(false)
    } catch {
      // TODO determine if we need to handle errors
      setIsOpen(false)
    }
  }

  const header = (
    <>
      <p>
        <b>Note: </b>Choosing to download account data will create a file that
        contains all data for account {accountId} for the given date range. This file
        will contain both PII and CI.
      </p>
      <fieldset className='o-form_fieldset block block__sub'>
        <legend className='h4'>Choose download options:</legend>
        <RadioButton
          id='include'
          name='contact-info-download'
          label='Include latest contact information for account holder'
          labelClassName=''
          labelInline
          isLarge
          inputRef={includeContactInfo}
        />
        <RadioButton
          id='exclude'
          name='contact-info-download'
          label='Do not include account holder contact information'
          labelClassName=''
          labelInline
          defaultChecked
          isLarge
        />
      </fieldset>
    </>
  )

  return (
    <div className='downloader'>
      <Button
        appearance='primary'
        label='Save account data'
        iconRight='download'
        onClick={onClick}
        size='default'
      />
      <DownloadModal
        open={isOpen}
        onClose={onClose}
        onDownload={onDownload}
        content={header}
        title='Download account data'
      />
    </div>
  )
}
