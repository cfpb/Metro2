import { Link, Outlet } from '@tanstack/react-router'
import { Heading, Layout, List, ListItem } from 'design-system-react'
import type { ReactElement } from 'react'
import './GuidePage.less'

export default function GuidePage(): ReactElement {
  const menuItems = [
    { name: '1. Overview of Metro2 Evaluator Tool', path: '/guide/' },
    { name: '2. Explore the Metro2 Interface', path: '/guide/explore' },
    {
      name: "3. Use Metro2's Advanced Table Features",
      path: '/guide/table'
    },
    {
      name: '4. Contributing to an Evaluator’s Metadata',
      path: '/guide/contribute'
    },
    {
      name: '5. Help Us Improve the Metro2 Evaluator Tool',
      path: '/guide/help-us'
    },
    { name: '6. Metro2 Administrator Features', path: '/guide/m2admin' }
  ]

  
  return (
    <Layout.Main layout='1-3'>
      <Layout.Wrapper>
        <Layout.Sidebar id='sidebar'>
          <Heading type='4'>Table of contents</Heading>
          <div>
            <List isUnstyled>
            {menuItems.map(item => (
                <ListItem>
                <Link
                key={item.name}
                to={item.path}
                className='o-secondary-nav__link o-secondary-nav__link--parent'
                activeOptions={{ exact: true }}
                activeProps={{ className: 'o-secondary-nav__link--current' }}>
                {item.name}
                </Link>
                </ListItem>
            ))}
            </List>
          </div>
        </Layout.Sidebar>
        <Layout.Content>
          <div className='content-pad'>
            <Outlet />
          </div>
        </Layout.Content>
      </Layout.Wrapper>
    </Layout.Main>
  )
}
