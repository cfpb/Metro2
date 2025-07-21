import { Heading, Divider, Paragraph } from 'design-system-react'
import type { ReactElement } from 'react'

export default function Admin(): ReactElement {
  return (
    <div className='content-pad'>
      <Heading type='2' className='h1'>
        Metro2 Administrator Features
      </Heading>

      <Divider />

      <Paragraph isLead />
      <Paragraph>
      Some features, such as adding users to an event and adding new data to the tool to be parsed and evaluated, are only available to administrators of the Metro 2 evaluator tool. 
      </Paragraph>

      <Heading type='3' className='h2'>
        Assign users to event
      </Heading>

      <Paragraph>
        Follow the steps listed below for access to the Metro2 Evaluator tool. You can
        &quot;right click&quot; (control-click on Macs) on the screenshots for a
        larger view of any image.
      </Paragraph>

      <Heading type='4'>Step 1</Heading>

      <Paragraph>Click on “Metro2 events” in the lefthand navigation.</Paragraph>
      <img
        src='/images/guide/admin_1.png'
        alt='Step 1'
      />

      <Heading type='4'>Step 2</Heading>

      <Paragraph>Select the event you want to assign users to.</Paragraph>
      <img
        src='/images/guide/admin_2.png'
        alt='Step 2'
      />

      <Heading type='4'>Step 3</Heading>

      <Paragraph>
        Under “Available members” select the user(s) you want to assign, click the
        right-facing arrow to add them to “Chosen members”.
      </Paragraph>
      <img
        src='/images/guide/admin_3.png'
        alt='Step 3'
      />

      <Heading type='4'>Step 4</Heading>

      <Paragraph>Press the “Save” button to save your changes.</Paragraph>
      <img
        src='/images/guide/admin_4.png'
        alt='Step 4'
      />

      <Heading type='4'>Step 5</Heading>

      <Paragraph>
        Afterwards, when a user goes to the Metro 2 link (in the first set of
        bullets), they’ll see the event(s) they’ve been assigned to
      </Paragraph>
      <img
        src='/images/guide/admin_5.png'
        alt='Step 5'
      />
    </div>
  )
}
