import { Button, Link as CFPBLink, Icon, LinkText } from 'design-system-react'
import type { ReactElement } from 'react'
import { useState } from 'react'
import { acceptPIIWarning, hasAcceptedPIIWarning } from 'utils/utils'
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
        This is a Consumer Financial Protection Bureau (CFPB) information system. The
        CFPB is an agency of the United States Government. CFPB information systems
        are provided for the processing of official information only. Unauthorized or
        improper use of this system may result in administrative action, as well as
        civil and criminal penalties.
      </p>

      <p>
        You must only access information for your role as authorized and you may not
        capture, copy, upload, download, print, transmit, or store information
        contained in this system without an authorized purpose. Because this is a
        CFPB information system, you have no reasonable expectation of privacy
        regarding any communication or data transiting or stored on this information
        system. All data contained on CFPB information systems is owned by CFPB and
        your use of the CFPB information system serves as your consent to your usage
        being monitored, intercepted, recorded, read, copied, captured or otherwise
        audited in any manner, by authorized personnel, including but not limited to
        employees, contractors and/or agents of the United States Government.
      </p>

      <p>
        <strong>
          I understand that by using this system, I will be accessing Personally
          Identifiable Information (PII) and Confidential Information (CI) and I
          understand my responsibilities to safeguard all CFPB information.
        </strong>{' '}
        I understand that this data is sensitive and is for authorized internal use
        only. I understand that unauthorized access, disclosure, and use of PII and
        CI constitutes a breach. All suspected and confirmed breaches of PII and CI
        must be reported through the{' '}
        <CFPBLink
          hasIcon
          href='https://cfpbprod.servicenowservices.com/servicecenter'>
          <LinkText>Service Center</LinkText>
          <Icon name='external-link' />
        </CFPBLink>{' '}
        or to the CFPB Privacy Office at{' '}
        <CFPBLink hasIcon href='mailto:privacy@cfpb.gov'>
          <LinkText>privacy@cfpb.gov</LinkText>
          <Icon name='email' />
        </CFPBLink>
        .
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
