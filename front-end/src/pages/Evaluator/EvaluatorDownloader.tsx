import Modal from 'components/DownloadCSV'
import { Button } from 'design-system-react'
import type { ReactElement} from 'react';
import { useState } from 'react'

export default function EvaluatorDownloader({}): ReactElement {
  const [isOpen, setIsOpen] = useState(false)

  const downloadCSV = () => {
    // TODO: this is a temporary hack to test the download functionality
    window.location.assign('/api/events/1/evaluator/Bankruptcy-DOFD-4/csv/')
    // TODO: consider approach for dismissing modal on download
    // Wait briefly before closing modal
    // The file dialog or automatic download (depending on user's browser settings)
    // might not be instantaneous and we don't want the modal to disappear before
    // anything else happens
    // Maybe show a spinner on button?
    setTimeout(() => {
      setIsOpen(false)
    }, 1000)
  }

  return (
    <div className='u-mt15 u-mb30'>
      <Button
        appearance='primary'
        label='Download evaluator results'
        iconRight='download'
        onClick={() => setIsOpen(true)}
        size='default'
      />
      <Modal
        open={isOpen}
        onClose={() => setIsOpen(false)}
        onDownload={downloadCSV}
      />
      <div id='portal' />
    </div>
  )
}
