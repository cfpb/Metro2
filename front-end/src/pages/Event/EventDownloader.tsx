import { Button } from 'design-system-react'
import type { ReactElement } from 'react'
import { downloadData, generateDownloadData } from 'utils/utils'

export default function EventDownloader({fields, rows, headerLookup, eventName}): ReactElement {
  const onClick = () => {
    const csv = generateDownloadData(fields, rows, headerLookup)
    const fileName = `${eventName}.csv`
    downloadData(csv, fileName)
  }

  return (
    <div className='downloader'>
      <Button
        appearance='primary'
        label='Download summary'
        iconRight='download'
        onClick={onClick}
        size='default'
      />
      <div id='portal' />
    </div>
  )
}
