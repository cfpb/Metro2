import { Divider, Heading, Paragraph } from 'design-system-react'
import type { ReactElement } from 'react'

export default function Overview(): ReactElement {
  return (
    <div className='content-pad'>
      <Heading type='2' className='h1'>
        Overview of Metro 2 Evaluator Tool
      </Heading>

      <Divider />

      <div>
        <Paragraph isLead />
        <Paragraph>
        The Metro 2 evaluator tool was developed to find inaccuracies in credit reporting data. This credit reporting information is in a format governed by the Consumer Data Industry Association (CDIA) called Metro2. Metro2 is almost universally used by furnishers. Metro2 details how loan information such as account type, account status, payments, and payment history can be reported to credit reporting agencies, such as Experian, Equifax, and Transunion. Any inaccuracy in credit reporting data can have ripple effects, affecting someone’s credit score and their ability to seek credit, causing real monetary harm. The Fair Credit Reporting Act (FCRA) enforces the accurate reporting of that credit information, and fair adjudication of consumer disputes.
        </Paragraph>
        <Paragraph>
        The Metro 2 evaluator tool has two goals:
        </Paragraph>

        <ul>
          <li>
          The first is to parse Metro-2 data from a fixed-width format, where every row is a tradeline and every column is a data field, and store it in a database, accessible for further exploration and analysis.
          </li>
          <li>
          The second goal is to evaluate these large volumes of consumer records for violations of the Fair Credit Reporting Act (FCRA). The process for determining which inaccuracies to check for can be up to the user. For reference, we’ve written approximately 100 logic checks (or evaluators) to identify inaccuracies in the data. The tradelines that do not pass logic checks are recorded. Using the tool’s interface, users can explore the inconsistencies in a set of Metro 2 data.
          </li>
        </ul>    
      </div>

      <Heading type='3' className='h2'>
        How the Metro2 tool works
      </Heading>
      <div>
        <Paragraph>
        For any given data set, this is the basic process that the Metro 2 evaluator tool uses to prepare data for analysis: 
        </Paragraph>

        <ol>
          <li>
          <b>Parse the data:</b> This is the process by which we ingest the raw Metro2-formatted data files and store the data into our tool’s database. If the files are not formatted correctly, sometimes they cannot be parsed. In that circumstance, you may need to troubleshoot and manually adjust the files or try again with corrected data files. 
          </li>

          <li>
            <b>Run evaluators:</b> The Metro 2 evaluator tool runs logic checks (or evaluators) to identify inaccuracies in the data. It runs all checks on a dataset and saves the results. The tradelines that do not pass logic checks are recorded.
          </li>

          <li>
            <b>Assess inconsistencies:</b> After those steps are completed, the tool is ready for users to log in to the tool, view the results of the evaluators, and explore the data. Using the tool’s interface, users can then explore the inconsistencies in this set of Metro 2 data. Find more information about how to <a href="/guide/explore">navigate the tool</a> and <a href="/guide/m2admin">manage user permissions</a>. 
          </li>
        </ol>
    </div>
      
      <Heading type='3' className='h2'>
        Assumptions
      </Heading>
      <div>
        <Paragraph>
        To effectively use this tool, the following assumptions have been made. Organizations using the tool must:
        </Paragraph>

        <ul>
          <li>Have the technical support required to run it locally and customize it as needed </li>
          <li>Have individuals who are knowledgeable about the Fair Credit Reporting Act.</li>
          <li>Have access to the Consumer Data Industry Association’s Credit Reporting Resource Guide (CRRG), which provides detailed information on the Metro 2 data format. </li>
          <li>Create their own evaluators. Evaluators are small logic checks that look for inconsistencies in a set of Metro 2 data. They should be based on CRRG criteria.</li>
        </ul>
        </div>
    </div>
  )
}
