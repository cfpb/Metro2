import { generateDownloadData } from './downloads'

describe('generateDownloadData', () => {
  it('generates a CSV string', () => {
    const fields = ['company', 'model', 'start_date', 'end_date', 'number_produced']
    const headerMap = new Map([
      ['company', 'Company name'],
      ['number_produced', 'Number of units produced']
    ])
    const data = [
      {
        company: 'Tucker Corporation',
        model: 'Tucker 48',
        start_date: '1947',
        end_date: '1948',
        number_produced: 50
      },
      {
        company: 'Gordon Keeble',
        model: 'GK1',
        start_date: '1964',
        end_date: '1967',
        number_produced: 100
      },
      {
        company: 'DeLorean Motor Company',
        model: 'DMC-12',
        start_date: '1981',
        end_date: '1982',
        number_produced: 9000
      }
    ]

    const header = 'Company name,Model,Start date,End date,Number of units produced'
    const body =
      'Tucker Corporation,Tucker 48,1947,1948,50\nGordon Keeble,GK1,1964,1967,100\nDeLorean Motor Company,DMC-12,1981,1982,9000'
    const expectedOutput = [header, body].join('\n')

    expect(generateDownloadData(fields, data, headerMap)).toEqual(expectedOutput)
  })

  it('adds quotes to strings containing commas', () => {
    const fields = ['company', 'model', 'description']
    const headerMap = new Map([['company', 'Company name']])
    const data = [
      {
        company: 'Tucker Corporation',
        model: 'Tucker 48',
        description:
          'The Tucker 48 was an automobile created by Preston Tucker and briefly produced in Chicago, Illinois, in 1948.'
      },
      {
        company: 'Gordon Keeble',
        model: 'GK1'
      },
      {
        company: 'DeLorean Motor Company',
        model: 'DMC-12'
      }
    ]

    const header = 'Company name,Model,Description'
    const body =
      'Tucker Corporation,Tucker 48,"The Tucker 48 was an automobile created by Preston Tucker and briefly produced in Chicago, Illinois, in 1948."\nGordon Keeble,GK1,\nDeLorean Motor Company,DMC-12,'
    const expectedOutput = [header, body].join('\n')

    expect(generateDownloadData(fields, data, headerMap)).toEqual(expectedOutput)
  })

  it('joins arrays with commas and quotes any strings containing commas', () => {
    const fields = ['company', 'model', 'description', 'features']
    const headerMap = new Map([['company', 'Company name']])
    const data = [
      {
        company: 'Tucker Corporation',
        model: 'Tucker 48',
        description:
          'The Tucker 48 was an automobile created by Preston Tucker and briefly produced in Chicago, Illinois, in 1948.',
        features: ['roll bar', 'directional headlamp', 'perimeter frame']
      },
      {
        company: 'Gordon Keeble',
        model: 'GK1'
      },
      {
        company: 'DeLorean Motor Company',
        model: 'DMC-12'
      }
    ]

    const header = 'Company name,Model,Description,Features'
    const body =
      'Tucker Corporation,Tucker 48,"The Tucker 48 was an automobile created by Preston Tucker and briefly produced in Chicago, Illinois, in 1948.","roll bar, directional headlamp, perimeter frame"\nGordon Keeble,GK1,,\nDeLorean Motor Company,DMC-12,,'
    const expectedOutput = [header, body].join('\n')

    expect(generateDownloadData(fields, data, headerMap)).toEqual(expectedOutput)
  })
})
