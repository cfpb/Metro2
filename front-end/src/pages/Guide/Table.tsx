/* eslint-disable react/jsx-key */
import {
  Divider,
  Heading,
  Link,
  List,
  ListItem,
  Paragraph,
  Table
} from 'design-system-react'
import type { ReactElement } from 'react'

export default function Features(): ReactElement {
  return (
    <div className='content-pad'>
      <Heading type='2' className='h1'>
        3. Use Metro2&apos;s Advanced Table Features
      </Heading>

      <Divider />

      <Paragraph isLead />
      <Paragraph>
        The tables in the Metro2 evaluator tool can be navigated with either a mouse
        or keyboard. You also can resize, reorder, pin, and sort multiple columns.
      </Paragraph>

      <Heading type='3' className='h2'>
        3.1 Navigate tables
      </Heading>

      <Paragraph>
        <b>Across cells:</b> You can use the{' '}
        <span className='hightlight'>[Tab]</span> key as well as arrow keys to
        navigate around the table with only a keyboard. Use the arrow keys (← ↑ → ↓)
        to move the focus up, down, left and right.
      </Paragraph>
      <Paragraph>
        <b>To get to the end of a row or column:</b> Use{' '}
        <span className='hightlight'>[^ Ctrl]</span> +
        <span className='hightlight'>[←]</span> to move to the start of the line, and{' '}
        <span className='hightlight'>[^ Ctrl]</span> +{' '}
        <span className='hightlight'>[→]</span>
        to move to the end. Use <span className='hightlight'>[^ Ctrl]</span> +{' '}
        <span className='hightlight'>[↑]</span> to move to the top of a column, and{' '}
        <span className='hightlight'>[^ Ctrl]</span> +{' '}
        <span className='hightlight'>[↓]</span> to move to the bottom. (On Macs,
        press <span className='hightlight'>[Command]</span> instead of{' '}
        <span className='hightlight'>[^ Ctrl]</span>.)
      </Paragraph>
      <Paragraph>
        <b>To quickly go to the first or last row:</b> Use{' '}
        <span className='hightlight'>[Home]</span> to go to the first row and{' '}
        <span className='hightlight'>[End]</span> to get to the last row of the
        table. On Macs, use <span className='hightlight'>[Function]</span> +{' '}
        <span className='hightlight'>[←]</span> or{' '}
        <span className='hightlight'>[Function]</span> +{' '}
        <span className='hightlight'>[→]</span>.
      </Paragraph>
      <Paragraph>
        <b>To scroll pages:</b> Use <span className='hightlight'>[Page Up]</span> and{' '}
        <span className='hightlight'>[Page Down]</span> to move the scroll up and
        down by one page.
      </Paragraph>

      <Heading type='3' className='h2'>
        3.2 Use Column Features
      </Heading>
      <div className='features'>
        <Table
          columns={['Column Feature', 'Mouse navigation', 'Keyboard navigation']}
          // @ts-expect-error DSR issue
          rows={[
            [
              'Pin',
              <div>
                <p>
                  It is possible to pin a column by moving the column in the
                  following ways:
                </p>
                <List>
                  <ListItem>
                    When no columns are pinned, drag the column you want to pin to
                    the left or right edge of the grid and wait for approximately one
                    second. The grid will then create a pinned area and place the
                    column into it.
                  </ListItem>
                  <ListItem>
                    When columns are already pinned, simply drag any additional
                    columns you want to pin into the existing pinned area.
                  </ListItem>
                  <ListItem>
                    To unpin columns, simply drag them away from the pinned area.
                  </ListItem>
                </List>
              </div>,
              'N/A'
            ],
            [
              'Reorder',
              'Click in an open space in the column header and drag to move a column to a new position.',
              <div>
                <p>
                  When focused on a columm header, you can use{' '}
                  <span className='hightlight'>[Shift]</span> +{' '}
                  <span className='hightlight'>[←]</span> or{' '}
                  <span className='hightlight'>[Shift]</span> +{' '}
                  <span className='hightlight'>[→]</span> to move the column to a new
                  position.
                </p>
              </div>
            ],
            [
              'Resize',
              'All columns can be resized by dragging the top right portion of the column. You can also click and drag the column separators.',
              <div>
                <p>
                  When focused on a column header, you can use{' '}
                  <span className='hightlight'>[Alt]</span> +{' '}
                  <span className='hightlight'>[←]</span> or{' '}
                  <span className='hightlight'>[Alt]</span> +{' '}
                  <span className='hightlight'>[→]</span> to increase or decrease
                  column size. For Mac users,{' '}
                  <span className='hightlight'>[Option]</span> +{' '}
                  <span className='hightlight'>[←]</span> or{' '}
                  <span className='hightlight'>[→]</span>
                </p>
              </div>
            ],
            [
              'Sort',
              'Click on a column header to sort the column.',
              <div>
                <p>
                  When the focus is on the column header, you can hit{' '}
                  <span className='hightlight'>[Enter]</span> (or{' '}
                  <span className='hightlight'>[Return]</span> on a Mac) to sort.
                </p>
              </div>
            ],
            [
              'Sort multiple columns',
              <div>
                It&apos;s also possible to sort by multiple columns. This lets you
                first sort by one column (the primary sort) and then sort within
                those groups by another column (the secondary sort) and so on. To
                sort an additional column, hold{' '}
                <span className='hightlight'>[Shift]</span> while you click the
                column header.
              </div>,
              <div>
                <p>
                  When the focus is on the column header, you can hold{' '}
                  <span className='hightlight'>[Shift]</span> +
                  <span className='hightlight'>[Enter]</span> (or{' '}
                  <span className='hightlight'>[Return]</span> on a Mac) to sort
                  additional columns.
                </p>
              </div>
            ]
          ]}
        />
      </div>
      <Paragraph>
        Any changes you make to the order, size, sorting, or pinning of columns in
        the Metro2 evaluator tool are for your current session. Subsequent visits
        will have the columns reset to the default orientation
      </Paragraph>
      <Paragraph>
        Note: We use a 3rd party open source table which supports accessibility
        natively. To learn more about use the links below.
      </Paragraph>
      <Paragraph>
        <Link href='https://www.ag-grid.com/react-data-grid/accessibility/'>
          https://www.ag-grid.com/react-data-grid/accessibility/
        </Link>
      </Paragraph>
      <Paragraph>
        <Link href='https://www.ag-grid.com/react-data-grid/keyboard-navigation/#'>
          https://www.ag-grid.com/react-data-grid/keyboard-navigation/
        </Link>
      </Paragraph>
    </div>
  )
}
