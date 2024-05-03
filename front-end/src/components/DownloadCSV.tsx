import {
  Button,
  ButtonGroup,
  Checkbox,
  Heading,
  Link,
  Paragraph
} from 'design-system-react'
import type { ReactElement } from 'react'
import React from 'react'
import ReactDom from 'react-dom'
import CFPBLogo from '../../public/images/logo_237x50@2x.png'

const MODAL_STYLES = {
  position: 'fixed',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  backgroundColor: '#fff',
  padding: '2rem',
  zIndex: 1000
}

const OVERLAY_STYLES = {
  position: 'fixed',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  backgroundColor: 'rgba(0, 0, 0, .7)',
  zIndex: 1000
}

interface DownloadModalProperties {
  open: boolean
  onClose: () => void
  onDownload: () => void
}

export default function Modal({
  open,
  onClose,
  onDownload
}: DownloadModalProperties): ReactElement | null {
  const [isChecked, setIsChecked] = React.useState(false)
  const handleChange = () => {
    setIsChecked(!isChecked)
  }

  if (!open) return null

  return ReactDom.createPortal(
    <>
      <div style={OVERLAY_STYLES} />
      <div style={MODAL_STYLES}>
        <img className='o-header_logo-img' src={CFPBLogo} alt='CFPB Logo' />
        <h1 className='u-mt15'>Create .csv file</h1>
        <Paragraph>
          <Heading type='2'>Personally identifiable information:</Heading>
          <Checkbox
            id='confirmPII'
            isLarge
            checked={isChecked}
            label='I confirm that I am knowingly downloading PII or CI and understand that I am responsible for safeguarding this data.'
            onChange={handleChange}
          />
        </Paragraph>

        <Paragraph>
          <Heading type='2'>
            Confirmation of ability to d/l PII or CI Statement:
          </Heading>

          <Paragraph>
            I understand that by downloading data from this system, I will be
            accessing Personally Identifiable Inforamtion (PII) and Confidential
            Information (CI).
          </Paragraph>

          <Paragraph>
            I confirm thta I have an authorized need to access this data and that I
            understand my respomsobilities to safeguard all CFPB information.
          </Paragraph>

          <Paragraph>
            I agree to only save downloaded data in an access-controlled location
            within the CFPB network and I will not share sata with anyone that is not
            authorized and does not have a need-to-know.
          </Paragraph>

          <Paragraph>
            I understand that this data is sensitive and for internal use only.
          </Paragraph>

          <Paragraph>
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
          </Paragraph>
        </Paragraph>

        <ButtonGroup>
          <Button
            appearance='primary'
            id='downloadCSV'
            iconRight='download'
            disabled={!isChecked}
            label='Save file'
            data-testid='csv-download-button'
            className='a-btn a-btn__full-on-xs'
            onClick={onDownload}
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
      </div>
    </>,
    document.getElementById('portal')! // assert element is not null
  )
}
