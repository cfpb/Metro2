import { ButtonGroup, Link as CFPBLink } from '@cfpb/design-system-react'
import { ADMIN_EMAIL } from '@src/config'
import { Link } from '@src/utils/DSRLink'
import { useRouterState } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import './ErrorMessage.scss'

interface ErrorMessageProperties {
  title: string
  description: string
  type?: string
}

export default function ErrorMessage({
  title,
  description,
  type = '500'
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
        <ButtonGroup>
          <Link asButton to='/' data-testid='back-button'>
            Back to Metro 2 home page
          </Link>
          {ADMIN_EMAIL ? (
            <CFPBLink
              asButton
              iconRight='email'
              // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
              href={`mailto:${ADMIN_EMAIL ?? ''}?subject=${type}%20Error%20at%20%22${currentPath}%22`}
              data-testid='contact-link'>
              Contact an administrator
            </CFPBLink>
          ) : undefined}
        </ButtonGroup>
      </div>
    </div>
  )
}
