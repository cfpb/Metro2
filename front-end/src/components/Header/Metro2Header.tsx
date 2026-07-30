import { Link as DSRLink, Header } from '@cfpb/design-system-react'
import { ReactElement } from 'react'
const showCFPBHeader =
  import.meta.env.VITE_SHOW_CFPB_HEADER === 'true' ? true : false

interface HeaderProps {
  showCFPBHeader?: boolean
}

export function Metro2Header({ showCFPBHeader = false }: HeaderProps): ReactElement {
  return showCFPBHeader ? (
    <Header
      href='/'
      links={[
        <DSRLink key='guide' to='/guide'>
          User guide
        </DSRLink>
      ]}
    />
  ) : (
    <header className='row row--action' data-testid='metro2-header'>
      <h1 className='h4 u-mb0'>
        <DSRLink to='/' className='a-link'>
          Metro2 Evaluator Tool
        </DSRLink>
      </h1>
      <div className='links'>
        <DSRLink to='/guide' className='nav-item'>
          Need help? See the user guide
        </DSRLink>
      </div>
    </header>
  )
}

export const M2Header = <Metro2Header showCFPBHeader={showCFPBHeader} />
