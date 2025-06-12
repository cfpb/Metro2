import { Button, ButtonGroup, Checkbox, Link } from 'design-system-react'
import type { ReactElement } from 'react'
import { useEffect, useState } from 'react'
import { Modal, ModalFooter } from './Modal'

interface DownloadModalProperties {
  open: boolean
  onClose: () => void
  onDownload: () => Promise<void>
  content?: ReactElement | null
  title?: string | null
  buttonText?: string
  privacyAuthorizationHeader?: string
}

export default function DownloadModal({
  open,
  onClose,
  onDownload,
  title = 'Create .csv file',
  buttonText = 'Save file',
  privacyAuthorizationHeader = 'Confirmation of ability to download PII or CI',
  content = null
}: DownloadModalProperties): ReactElement | null {
  const [isChecked, setIsChecked] = useState(false)
  const [isDownloading, setIsDownloading] = useState(false)

  useEffect(() => {
    setIsChecked(false)
    setIsDownloading(false)
  }, [open])

  const onChange = (): void => {
    setIsChecked(!isChecked)
  }

  const onClick = (): void => {
    setIsDownloading(true)
    // eslint-disable-next-line @typescript-eslint/no-floating-promises
    onDownload()
  }

  return (
    <Modal open={open} onClose={onClose}>
      <h1 className='h3'>{title}</h1>
      <div className='block block__sub'>{content}</div>
      <fieldset className='o-form_fieldset block block__sub'>
        <legend className='h4'>{privacyAuthorizationHeader}</legend>
        <p>
          I understand that by downloading data from this system, I will be accessing
          Personally Identifiable Information (PII) and Confidential Information
          (CI).
        </p>

        <p>
          I confirm that I have an authorized need to access this data and that I
          understand my responsibilities to safeguard all CFPB information.
        </p>

        <p>
          I agree to only save downloaded data in an access-controlled location
          within the CFPB network and I will not share data with anyone that is not
          authorized and does not have a need-to-know.
        </p>

        <p>I understand that this data is sensitive and for internal use only.</p>

        <div className='modal-p-padding'>
          <p>
            I understand that unauthorized access, disclosure, and use of PII and CI
            constitutes a breach. All suspected and confirmed breaches of PII and CI
            must be reported through the{' '}
            <Link
              href='https://cfpbprod.servicenowservices.com/servicecenter?id=sd_home'
              target='_blank'
              rel='noreferrer'>
              Service Center
            </Link>{' '}
            or to the CFPB Privacy Office at{' '}
            <Link href='mailto:privacy@cfpb.gov'>privacy@cfpb.gov</Link>
          </p>
        </div>
        <div className='u-mt15'>
          <Checkbox
            id='confirmPII'
            isLarge
            checked={isChecked}
            label='I confirm that I am knowingly downloading PII or CI and understand that I am responsible for safeguarding this data.'
            onChange={onChange}
          />
        </div>
      </fieldset>

      <ModalFooter>
        <ButtonGroup>
          <Button
            appearance='primary'
            id='downloadCSV'
            iconRight={isDownloading ? 'updating' : 'download'}
            disabled={!isChecked || isDownloading}
            label={isDownloading ? 'Downloading...' : buttonText}
            data-testid='csv-download-button'
            className='a-btn a-btn__full-on-xs'
            onClick={onClick}
            size='default'
          />

          <Button
            appearance='primary'
            asLink
            label='Cancel'
            className='a-btn a-btn__link a-btn__full-on-xs'
            onClick={onClose}
            size='default'
          />
        </ButtonGroup>
      </ModalFooter>
    </Modal>
  )
}