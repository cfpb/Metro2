import { Heading, Divider, Paragraph } from 'design-system-react'
import type { ReactElement } from 'react'

export default function HelpUs(): ReactElement {
  return (
    <div className='content-pad'>
      <Heading type='2' className='h1'>
        5. Help Us Improve the Metro2 Evaluator Tool
      </Heading>

      <Divider />
      <div>
        <Paragraph isLead />
        <Paragraph>
          Do you have ideas that for the Metro 2 evaluator tool that would make if
          more useful for you? We would love to hear your ideas. This could be things
          like:
        </Paragraph>

        <Paragraph>
          Which columns are visible in the UI by default and their position in the
          table. The current categories are a best guess at what might be useful.
          Would you like to see something else?
        </Paragraph>

        <Paragraph>
          <b>Send us an email using the following email address:</b>
        </Paragraph>

        <Paragraph>
          {' '}
          <a href='mailto:Metro2Admin@cfpb.gov'>Metro2Admin@cfpb.gov</a>
        </Paragraph>

        <Paragraph>In your email please include the details of your idea:</Paragraph>

        <Paragraph>
          <b>Type of request:</b> Describe if it is a one-off feature or a series of
          features{' '}
        </Paragraph>
        <Paragraph>
          <b>Who is requesting this:</b> Tell us who you are and what team you are on
          so we can follow up{' '}
        </Paragraph>
        <Paragraph>
          <b>Describe the problem you are having:</b> Explain for us what isn’t
          working or could be improved and why.{' '}
        </Paragraph>
        <Paragraph>
          {' '}
          <b>Suggest how the problem may be solved:</b> Give use your idea for a
          solution(s){' '}
        </Paragraph>
        <Paragraph>
          <b>Urgency:</b> Describe how urgent this request is and let us know why{' '}
        </Paragraph>
      </div>
    </div>
  )
}
