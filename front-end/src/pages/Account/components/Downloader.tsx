import { Button, RadioButton } from '@cfpb/design-system-react'
import DownloadModal from '@src/components/Modal/DownloadModal'
import type Event from '@src/types/Event'
import { useQueryClient } from '@tanstack/react-query'
import { Workbook } from 'exceljs'
import type { ReactElement } from 'react'
import { useRef, useState } from 'react'

import ACCOUNT_HOLDER_FIELDS from '@src/constants/accountHolderFields'
import EVENT_FIELDS from '@src/constants/eventFields'
import M2_FIELD_NAMES from '@src/constants/m2FieldNames'
import { accountHolderQueryOptions } from '@src/queries/accountHolder'
import type AccountRecord from '@src/types/AccountRecord'
import { downloadData } from '@src/utils/downloads'
import getHeaderName from '@src/utils/getHeaderName'

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
  const [includeContactInfo, setIncludeContactInfo] = useState('exclude')

  const includeContactInfoRadioButton = useRef<HTMLInputElement>(null!)

  const onClose = (): void => {
    setIsOpen(false)
    setIncludeContactInfo('exclude')
  }

  const onClick = (): void => {
    setIsOpen(true)
  }

  const onChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    setIncludeContactInfo(event.target.value)
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
    if (includeContactInfoRadioButton.current?.checked) {
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
      downloadData(
        buffer as unknown as Buffer,
        `${eventData.name}_${accountId}.xlsx`,
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      )
      onClose()
    } catch {
      // TODO determine if we need to handle errors
      onClose()
    }
  }

  const header = (
    <>
      <fieldset className='o-form__fieldset block block--sub'>
        <legend className='h4'>Choose download options:</legend>
        <p>
          Choosing to download account data will create a file that contains all data
          for account {accountId} for the given date range. This file will contain
          both Personally Identifiable Information (PII) and Confidential Information
          (CI).
        </p>
        <RadioButton
          id='include'
          value='include'
          name='contact-info-download'
          label='Include latest contact information for account holder'
          labelClassName=''
          isLabelInline
          isLarge
          checked={includeContactInfo === 'include'}
          onChange={onChange}
          inputRef={includeContactInfoRadioButton}
        />
        <RadioButton
          id='exclude'
          value='exclude'
          name='contact-info-download'
          label='Do not include account holder contact information'
          labelClassName=''
          isLabelInline
          checked={includeContactInfo === 'exclude'}
          onChange={onChange}
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
        title='Save account data'
        copyText="Copy the link to this account's data."
        content={header}
      />
    </div>
  )
}
