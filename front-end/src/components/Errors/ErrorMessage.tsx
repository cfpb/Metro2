import { Link, useRouterState } from '@tanstack/react-router'
import { Link as CFPBLink, Icon } from 'design-system-react'
import type { ReactElement } from 'react'
import './ErrorMessage.less'

interface ErrorMessageProperties {
  title: string
  description: string
  mailbox: string
  errorType: string
}

export default function ErrorMessage({
  title,
  description,
  mailbox,
  errorType
}: ErrorMessageProperties): ReactElement {
  const router = useRouterState()
  const currentPath = router.location.pathname

  return (
    <div className='error-container content-row' data-testid='error-container'>
      <div data-testid='error-message' className='error-message'>
        <h2 data-testid='error-title' className='h1'>
          {title}
        </h2>
        <p data-testid='error-description'>{description}</p>
        <div className='m-btn-group'>
          <Link to='/' className='a-btn a-btn__full-on-xs' data-testid='back-button'>
            Back to Metro 2 home page
          </Link>

{/*     Update "mailbox" in ErrorList and NotFound files before enabling the following code for admin contact   
          <CFPBLink
            className='a-btn a-btn__link a-btn__full-on-xs'
            hasIcon
            href={`mailto:${mailbox}?subject=${errorType}%20Error%20at%20%22${currentPath}%22`}
            data-testid='contact-link'>
            Contact an administrator
            <Icon name='email' />
          </CFPBLink> */}
        </div>
      </div>
    </div>
  )
}
