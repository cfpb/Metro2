import { Button } from '@cfpb/design-system-react'
import { acceptPIIWarning, hasAcceptedPIIWarning } from '@src/utils/cookies'
import DOMPurify from 'dompurify'
import type { ReactElement } from 'react'
import { useState } from 'react'
import { Modal, ModalFooter } from './Modal'

const warningText = DOMPurify.sanitize(import.meta.env.VITE_PII_WARNING_TEXT)

export default function WarningModal(): ReactElement | null {
  const [isOpen, setIsOpen] = useState(!hasAcceptedPIIWarning())

  if (!isOpen) return null

  const onClick = (): void => {
    acceptPIIWarning()
    setIsOpen(false)
  }

  return (
    <Modal open={isOpen} interactionRequired data-testid='warning-modal'>
      <h1 className='h3 u-mb30'>Warning</h1>
      <div
        data-testid='warning-text'
        dangerouslySetInnerHTML={{ __html: warningText }}></div>
      <ModalFooter>
        <Button
          appearance='primary'
          id='accept'
          label='Accept and continue to PII'
          data-testid='accept-warning-button'
          className='a-btn a-btn--full-on-xs'
          onClick={onClick}
          size='default'
        />
      </ModalFooter>
    </Modal>
  )
}
