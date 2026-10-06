import { Button, Icon } from '@cfpb/design-system-react'
import CopyUrl from '@src/components/CopyUrl'
import { Modal, ModalFooter } from '@src/components/Modal/Modal'
import type { ReactElement } from 'react'

interface DownloadErrorModalProperties {
  open: boolean
  onClose?: () => void
}
export default function DownloadErrorModal({
  open,
  onClose
}: DownloadErrorModalProperties): ReactElement {
  const onClick = (): void => {
    onClose?.()
  }

  return (
    <Modal
      open={open}
      onClose={onClick}
      data-testid='download-error-modal'
      className='download-error-modal '>
      <div className='heading-with-icon u-mb10'>
        <Icon name='warning-round' size='32px' />
        <h1>Download failed</h1>
      </div>
      <p>
        Your download failed. We recommend you save the URL and try again later. If
        it&apos;s still a problem, please contact an administrator.
      </p>
      <CopyUrl />
      <ModalFooter>
        <Button
          appearance='primary'
          id='close'
          label='Okay'
          data-testid='close-error-modal'
          className='a-btn a-btn--full-on-xs'
          onClick={onClick}
          size='default'
        />
      </ModalFooter>
    </Modal>
  )
}
