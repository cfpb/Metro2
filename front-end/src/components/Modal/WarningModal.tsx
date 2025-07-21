import { Button } from 'design-system-react'
import type { ReactElement } from 'react'
import { useState } from 'react'
import { acceptPIIWarning, hasAcceptedPIIWarning } from 'utils/cookies'
import { Modal, ModalFooter } from './Modal'

export default function WarningModal(): ReactElement | null {
  const [isOpen, setIsOpen] = useState(!hasAcceptedPIIWarning())

  if (!isOpen) return null

  const onClick = (): void => {
    acceptPIIWarning()
    setIsOpen(false)
  }

  return (
    <Modal open={isOpen} interactionRequired>
      <h1 className='h3 u-mb30'>Warning</h1>
      <p>
        I understand that by using this system, I will be accessing Personally
        Identifiable Information (PII) and Confidential Information (CI) and I
        understand my responsibilities to safeguard all this information.
      </p>
      <ModalFooter>
        <Button
          appearance='primary'
          id='accept'
          label='Accept and continue to PII'
          data-testid='csv-download-button'
          className='a-btn a-btn__full-on-xs'
          onClick={onClick}
          size='default'
        />
      </ModalFooter>
    </Modal>
  )
}
