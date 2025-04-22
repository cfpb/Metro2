import { Button } from 'design-system-react'
import type { ReactElement } from 'react'
import type EvaluatorMetadata from 'types/Evaluator'
import { downloadData, generateDownloadData } from 'utils/utils'

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

  const onClick = (): void => {
    const csv = generateDownloadData(fields, rows, headerMap)
    const fileName = `${eventName}.csv`
    // eslint-disable-next-line @typescript-eslint/no-floating-promises
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
