import type { ReactElement } from 'react'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import Table from 'components/Table/Table'
import eventData from '../../fixtures/event.json'
import columnDefinitions from './columnDefinitions'
import type { EvaluatorMetadata } from './Event'

export default function EventPage(): ReactElement {
	const rowData = eventData.evaluators as EvaluatorMetadata[]

	return (
		<>
    	<LocatorBar heading={ eventData.name }
                  subhead={ `Data from ${ eventData.start_date } - ${ eventData.end_date }` }/>
			<div className='block'>
				<Table rows={ rowData } 
               columnDefinitions={ columnDefinitions }
               height='full' 
               resizableColumns={ false }/>
			</div>
		</>
	)
}
