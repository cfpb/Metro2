import { Divider, Heading, Paragraph } from 'design-system-react'
import type { ReactElement } from 'react'

export default function Contribute(): ReactElement {
  return (
    <div className='content-pad'>
      <Heading type='2' className='h1'>
        Contribute to an Evaluator&apos;s Metadata
      </Heading>

      <Divider />

      <Paragraph isLead />
      <Paragraph>
      The Metro 2 evaluator tool is meant to be extendable. You can create more evaluators, but you can also add metadata which helps to add context to the evaluators. Metadata contributed by users can add context, which will help make the tool easier to understand and more useful for everyone. As you use the tool, consider how your experience and knowledge about specific evaluators—and the FCRA—can help others. These categories of metadata may be helpful:  
      </Paragraph>

        <ul>
          <li>
            <b>Rationale:</b> Explains why the inconsistency found by this evaluator is a problem and describes what’s required for the account to be accurately furnished.
          </li>

          <li>
            <b>Potential harm:</b> Describes the negative impact this inconsistency might have on an individual’s credit.
          </li>

          <li>
            <b>Alternate explanation:</b> Describes any logical reasons for this inconsistency to exist when the account has been accurately furnished.
          </li>

          <li>
            <b>CRRG reference:</b> Includes references to specific sections of the Credit Reporting Resource Guide (CRRG) that may be useful for interpreting the results of this evaluator.
          </li>
        </ul>

      <Paragraph>
      If you’re a Metro 2 administrator, you can add information metadata directly to an evaluator. If you’re not, please email your contribution to your Metro 2 administrator for their review. 
      </Paragraph>

    </div>
  )
}
