
import type { ColDef, ValueFormatterParams } from 'ag-grid-community';
import type { EvaluatorMetadata } from './Event'

const columnDefinitions: ColDef<EvaluatorMetadata>[] = [
	{
		field: 'id',
		headerName: 'Inconsistency',
		type: 'wrappableText',
		valueFormatter: ( { value }: ValueFormatterParams): string => typeof value === 'string' ? value.toUpperCase() : ''
	},
	{
		field: 'description',
		headerName: 'Description',
		type: 'wrappableText',
		flex: 3
	}, 
	{
		field: 'category',
		headerName: 'Category',
		type: 'wrappableText',
		flex: 1
	}, 
	{
		field: 'hits',
		headerName: 'Total instances',
		type: 'formattedNumber',
		flex: 1,
	},
	{
		field: 'accounts',
		headerName: 'Total accounts',
		type: 'formattedNumber',
		flex: 1
	}
]

export default columnDefinitions
