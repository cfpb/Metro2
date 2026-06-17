import { Button, ButtonGroup, Checkbox } from '@cfpb/design-system-react'
import DOMPurify from 'dompurify'
import type { ReactElement } from 'react'
import { useState } from 'react'
import CopyUrl from '../CopyUrl'
import { Modal, ModalFooter } from './Modal'

interface DownloadModalProperties {
  open: boolean
  onClose?: () => void
  onDownload?: () => Promise<void> | void
  title?: string | null
  copyText?: string
  content?: ReactElement | null
  requirePrivacyAcknowledgment?: boolean
  privacyHeader?: string
  buttonText?: string
}

const downloadText = DOMPurify.sanitize(
  import.meta.env.VITE_DOWNLOAD_ACKNOWLEDGMENT_TEXT
)

/**
 * DownloadModal()
 *
 * A modal that provides some shared download functionality, including:
 *   - CopyUrl component
 *   - PII acknowledgment checkbox
 *   - Download button that is activated when privacy warning is acknowledged,
 *   - useEffect hook that updates state to clear the PII checkbox when the modal
 *     is closed by its parent component (modal is not visible when this happens)
 *
 * @param {boolean} open - Whether the modal is open or closed
 * @param {function} onClose - event handler for modal close button
 * @param {function} onDownload - event handler for modal download button
 * @param {string} title - Heading for the modal
 * @param {string} copyText - Descriptive text for the copy url section
 * @param {ReactElement} content - Any custom content for the modal
 * @param {boolean} requirePrivacyAcknowledgment - Whether to require privcay acknowledgment before download
 * @param {string} privacyHeader - Heading for privacy acknowledgment text
 * @param {string} buttonText - Text for the download button

 * @returns {ReactElement}
 */

export default function DownloadModal({
  open,
  onClose,
  onDownload,
  title = 'Create .csv file',
  copyText = 'Copy a link to this page',
  content = null,
  requirePrivacyAcknowledgment = true,
  privacyHeader = 'Confirmation of ability to download PII or CI',
  buttonText = 'Download file'
}: DownloadModalProperties): ReactElement | null {
  const [privacyMessageAcknowledged, setPrivacyMessageAcknowledged] = useState(false)

  const onChange = (): void => {
    setPrivacyMessageAcknowledged(!privacyMessageAcknowledged)
  }

  const onClickDownloadButton = (): void => {
    void onDownload?.()
  }

  const onCloseModal = (): void => {
    onClose?.()
    setPrivacyMessageAcknowledged(false)
  }

  return (
    <Modal open={open} onClose={onCloseModal}>
      <h1 className='h3'>{title}</h1>
      <div className='block block--sub'>
        <h4>Save a link for later</h4>
        <p>{copyText}</p>
        <CopyUrl />
      </div>
      <div className='block block--sub'>{content}</div>
      {requirePrivacyAcknowledgment && (
        <fieldset
          className='o-form__fieldset block block--sub'
          data-testid='download-acknowledgment'>
          <legend className='h4'>{privacyHeader}</legend>
          <p dangerouslySetInnerHTML={{ __html: downloadText }}></p>
          <div className='u-mt15'>
            <Checkbox
              id='confirmPII'
              isLarge
              checked={privacyMessageAcknowledged}
              data-testid='pii-checkbox'
              label='I confirm that I am knowingly downloading PII or CI and understand that I am responsible for safeguarding this data.'
              onChange={onChange}
            />
          </div>
        </fieldset>
      )}

      <ModalFooter>
        <ButtonGroup>
          <Button
            appearance='primary'
            id='downloadCSV'
            iconRight='download'
            disabled={requirePrivacyAcknowledgment && !privacyMessageAcknowledged}
            label={buttonText}
            data-testid='csv-download-button'
            className='a-btn a-btn--full-on-xs'
            onClick={onClickDownloadButton}
            size='default'
          />

          <Button
            appearance='primary'
            asLink
            label='Cancel'
            className='a-btn a-btn--link a-btn--full-on-xs'
            onClick={onCloseModal}
            size='default'
          />
        </ButtonGroup>
      </ModalFooter>
    </Modal>
  )
}
