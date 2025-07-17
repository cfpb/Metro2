/* eslint-disable react/jsx-key */
import { Divider, Heading, List, ListItem, Paragraph } from 'design-system-react'
import type { ReactElement } from 'react'

export default function Explore(): ReactElement {
  return (
    <div className='content-pad'>
      <Heading type='2' className='h1'>
        Explore the Metro2 Interface
      </Heading>
      <Divider />

      <Heading type='3' className='h2'>
        Events list
      </Heading>
      <div>
        <Paragraph>
        The event list is the main entry point into the Metro 2 application. It lists all the events that you are assigned to. 
        </Paragraph>
        <img
          src="/images/guide/event_list.png"
          alt='Events list'
          className='imageBorder'
        />

          <List isOrdered>
            {/* <React.Fragment key=".0"> */}
            <ListItem>
              <b>Application title: </b> Clicking on this text on any screen will take you back to this events page. You can think of it as the home button for the application.
            </ListItem>
            <ListItem>
              <b>User guide link: </b> Using the user guide link on any screen will open this page. If you have questions about the application, the user guide is a good place to start looking for information.
            </ListItem>
            <ListItem>
              <b>Welcome message: </b> The welcome message is a verification that you are logged in and using the correct account.
            </ListItem>
            <ListItem>
              <b>Event list: </b> The event list will contain all the events that have been assigned to you. Typically, the event list will contain name, the date range that this data covers, and a link to access the evaluator results for the event.
            </ListItem>
            {/* </React.Fragment> */}
          </List>
      </div>

      <Heading type='3' className='h2'>
        Evaluator list
      </Heading>
      <div>
        <Paragraph>
        The evaluator list page shows the results of having run evaluators on the data. This list contains all evaluators that identify inaccuracies in the data.
        </Paragraph>

        <img
          src="/images/guide/evaluator_list.png"
          alt='Evaluator list'
          className='imageBorder'
        />

        <List isOrdered>
          {/* <React.Fragment key=".0"> */}
          <ListItem>
            <b>Title bar: </b> Contains institution name and the date range covered by the Metro 2 data. It’s intended for wayfinding and to orient you to the event data you are seeing. 
          </ListItem>

          <ListItem>
            <b>Evaluator: </b> This column provides the names of the evaluators that found inconsistencies in the data. 
          </ListItem>

          <ListItem>
            <b>Description: </b>  This column includes a description of the logic check performed by each evaluator to help you understand the nature of the inconsistency found.
          </ListItem>

          <ListItem>
            <b>Categories: </b> This is the type of inconsistency that the evaluator identified. 
          </ListItem>

          <ListItem>
            <b>Total instances: </b> The total number of inconsistencies, or “hits,” recorded by this evaluator for this event.
          </ListItem>

          <ListItem>
            <b>Total accounts: </b> The number of unique accounts affected by this inconsistency for this event. 
          </ListItem>

          <ListItem>
            <b>Save results: </b> This lets you save a link to this URL or download the summary table shown on this screen in a .csv file. 
          </ListItem>

          {/* </React.Fragment> */}
        </List>
      </div>

      <Heading type='3' className='h2'>
        Single evaluator list
      </Heading>
      <div>
        <Paragraph>
        This view provides details about the logic check performed by the evaluator and the inaccuracies it found in the data.
        </Paragraph>
        <img
          src='/images/guide/single_eval_list.png'
          alt='Single evaluator list'
          className='imageBorder'
        />

          <List isOrdered>
            {/* <React.Fragment key=".0"> */}
            <ListItem>
              <b>Title bar: </b> Contains the name of the evaluator being shown on the page.
            </ListItem>

            <ListItem>
              <b>Details: </b> Details about the evaluator, including the date range for this event, the duration of when inconsistencies occurred, the total number of inconsistencies found, and the total number of accounts affected by the inconsistency.
            </ListItem>

            <ListItem>
              <b>Description: </b> A short description of the evaluator’s logic. It provides a high-level summary of the inconsistency found by the evaluator. 
            </ListItem>

            <ListItem>
              <b>Criteria evaluated: </b> A full description of the criteria being examined by this evaluator. The tradelines that do not pass logic checks are recorded. These are considered “hits,” and are included in the results table below. 
            </ListItem>

            <ListItem>
              <b>How to evaluate the results: </b> When available, this metadata provides more context for interpreting the evaluator results. This may include: the rationale behind why the data may contain this inconsistency, what type of potential harm to consumers may result from this inconsistency, links or references to the CRRG to provide more context about the data points, and alternative explanations for this inconsistency that may not result in consumer harm. 
            </ListItem>

            <ListItem>
              <b>Sample of results: </b> By default, a representative sample of up to 20 hits is shown for the evaluator. When an evaluator has more than 20 hits, a sample is taken from across the time frame of the event. Tabs let users switch from viewing a sample of results to being able to view and filter all the evaluator’s results.  
            </ListItem>

            <ListItem>
              <b>Results table: </b> The columns displayed in the table vary for different evaluators. It includes fields used by the evaluator, as well as supplementary data columns that may be helpful for determining the impact of the inaccuracy.
            </ListItem>

            <ListItem>
              <b>Save results: </b> This lets you save a link to this URL, download the sample of 20 results, or alternatively all the results for this evaluator in CSV format. Any filters you’ve applied will be included. 
            </ListItem>

            {/* </React.Fragment> */}
          </List>
      </div>

      <Heading type='3' className='h2'>
        Single account view
      </Heading>
      <div>
        <Paragraph>
        The page shows all data associated with an individual account number.
        </Paragraph>
        <img
          src='/images/guide/single_account_view.png'
          alt='Single account view'
          className='imageBorder'
        />

          <List isOrdered>
            {/* <React.Fragment key=".0"> */}
            <ListItem>
              <b>Title bar: </b> Contains the account number of the account being shown on the page.
            </ListItem>

            <ListItem>
              <b>Account details: </b> Information that generally does not change throughout the lifetime of an account, such as portfolio type, account type, and the date the account was opened. 
            </ListItem>

            <ListItem>
              <b>Contact information: </b> Clicking “show” reveals the contact information for the account holder, including name, address, and phone number.
            </ListItem>

            <ListItem>
              <b>Inconsistencies found: </b> List of all the evaluators that found inconsistencies in this account’s data. Account data table: This table shows all data associated with this account over time, in chronological order. Each row in the table is a “tradeline” from the Metro 2 data. 
            </ListItem>

            <ListItem>
              <b>Account data table: </b> This table shows all data associated with this account over time, in chronological order. Each row in the table is a “tradeline” from the Metro 2 data.
            </ListItem>

            <ListItem>
              <b>Save account data: </b> This lets you save a link to this URL or download the data contained in the table, as well as the contact information for the account holder, in Excel format (.xlsx).
            </ListItem>
            {/* </React.Fragment> */}
          </List>
      </div>
    </div>
  )
}
