import { Button, ButtonGroup, Checkbox } from '@cfpb/design-system-react'
import type { ReactElement } from 'react'
import { useEffect, useState } from 'react'
import { Modal, ModalFooter } from './Modal'

interface DownloadModalProperties {
  open: boolean
  onClose: () => void
  onDownload: () => Promise<void> | void
  content?: ReactElement | null
  title?: string | null
  copy?: string | null
  buttonText?: string
  privacyAuthorizationHeader?: string
  hidePII?: boolean
}

export default function DownloadModal({
  open,
  onClose,
  onDownload,
  title = 'Create .csv file',
  buttonText = 'Download file',
  privacyAuthorizationHeader = 'Confirmation of ability to download PII or CI',
  copy = 'I understand that by downloading data from this system, I will be accessing Personally Identifiable Information (PII) and Confidential Information (CI).',
  content = null,
  hidePII
}: DownloadModalProperties): ReactElement | null {
  const [isChecked, setIsChecked] = useState(false)

  useEffect(() => {
    if (hidePII) {
      setIsChecked(true)
    } else {
      setIsChecked(false)
    }
  }, [open, hidePII])

  const onChange = (): void => {
    setIsChecked(!isChecked)
  }

  const onClick = (): void => {
    // eslint-disable-next-line @typescript-eslint/no-floating-promises
    onDownload()
  }

  return (
    <Modal open={open} onClose={onClose}>
      <h1 className='h3'>{title}</h1>
      <div className='block block--sub'>{content}</div>
      {!hidePII && (
        <fieldset className='o-form__fieldset block block--sub'>
          <legend className='h4'>{privacyAuthorizationHeader}</legend>
          <p>{copy}</p>
          <div className='u-mt15'>
            <Checkbox
              id='confirmPII'
              isLarge
              checked={isChecked}
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
            disabled={!isChecked}
            label={buttonText}
            data-testid='csv-download-button'
            className='a-btn a-btn--full-on-xs'
            onClick={onClick}
            size='default'
          />

          <Button
            appearance='primary'
            asLink
            label='Cancel'
            className='a-btn a-btn--link a-btn--full-on-xs'
            onClick={onClose}
            size='default'
          />
        </ButtonGroup>
      </ModalFooter>
    </Modal>
  )
}
