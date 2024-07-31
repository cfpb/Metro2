import LocatorBar from 'components/LocatorBar/LocatorBar'
import { Layout } from 'design-system-react'
import type { ReactElement } from 'react'
import './GuidePage.less'

export default function GuidePage(): ReactElement {

  return (
    <>
      <Layout.Main layout="1-3">
      <Layout.Wrapper>
      < Layout.Sidebar id='sidebar'>
        <div>
          <ul>
            <li>
              Instructions for Metro 2

              <ul>
                <li>
                Item 1
                </li>
                <li>
                  Item 2
                </li>
                <li>
                  Item 3
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </Layout.Sidebar>
      <Layout.Content>
      <h3>
        Content
      </h3>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipisicing elit.
        Cum corrupti tempora nam nihil qui mollitia consectetur
        corporis nemo culpa dolorum! Laborum at eos deleniti
        consequatur itaque officiis debitis quisquam! Provident!
      </p>
      </Layout.Content>      
      </Layout.Wrapper>
      </Layout.Main>
    </>
  )
}