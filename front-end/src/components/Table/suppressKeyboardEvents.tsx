/* eslint-disable */
// @ts-nocheck
/**
 * AG Grid's default event handling excludes links within a table
 * from the tab order. This override allows keyboard navigation to
 * interactive elements output in cells by custom renderers.
 *
 * The code is borrowed from an example in the documentation here:
 * https://www.ag-grid.com/react-data-grid/keyboard-navigation/#custom-cell-component
 */

const GRID_CELL_CLASSNAME = 'ag-cell'

function getAllFocusableElementsOf(el: HTMLElement) {
  return [
    ...el.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
  ].filter(focusableEl => focusableEl.tabIndex !== -1)
}

const getEventPath: (event: Event) => HTMLElement[] = (event: Event) => {
  const path: HTMLElement[] = []
  let currentTarget: any = event.target
  while (currentTarget) {
    path.push(currentTarget)
    currentTarget = currentTarget.parentElement
  }
  return path
}

/**
 * Capture whether the user is tabbing forwards or backwards and suppress keyboard event if tabbing
 * outside of the children
 */
function suppressKeyboardEvent({ event }: SuppressKeyboardEventParams<any>) {
  const { key, shiftKey } = event
  const path = getEventPath(event)
  const isTabForward = key === 'Tab' && shiftKey === false
  const isTabBackward = key === 'Tab' && shiftKey === true

  let suppressEvent = false

  // Handle cell children tabbing
  if (isTabForward || isTabBackward) {
    const eGridCell = path.find(el => {
      if (el.classList === undefined) return false
      return el.classList.contains(GRID_CELL_CLASSNAME)
    })

    if (!eGridCell) {
      return suppressEvent
    }

    const focusableChildrenElements = getAllFocusableElementsOf(eGridCell)
    const lastCellChildEl = focusableChildrenElements.at(-1)
    const firstCellChildEl = focusableChildrenElements[0]

    // Suppress keyboard event if tabbing forward within the cell and the current focused element is not the last child
    if (focusableChildrenElements.length === 0) {
      return false
    }

    const currentIndex = focusableChildrenElements.indexOf(
      document.activeElement as HTMLElement
    )

    if (isTabForward) {
      const isLastChildFocused =
        lastCellChildEl && document.activeElement === lastCellChildEl

      if (!isLastChildFocused) {
        suppressEvent = true
        if (currentIndex !== -1 || document.activeElement === eGridCell) {
          event.preventDefault()
          focusableChildrenElements[currentIndex + 1].focus()
        }
      }
    }
    // Suppress keyboard event if tabbing backwards within the cell, and the current focused element is not the first child
    else {
      const cellHasFocusedChildren =
        eGridCell.contains(document.activeElement) &&
        eGridCell !== document.activeElement

      // Manually set focus to the last child element if cell doesn't have focused children
      if (!cellHasFocusedChildren) {
        lastCellChildEl.focus()
        // Cancel keyboard press, so that it doesn't focus on the last child and then pass through the keyboard press to
        // move to the 2nd last child element
        event.preventDefault()
      }

      const isFirstChildFocused =
        firstCellChildEl && document.activeElement === firstCellChildEl
      if (!isFirstChildFocused) {
        suppressEvent = true
        if (currentIndex !== -1 || document.activeElement === eGridCell) {
          event.preventDefault()
          focusableChildrenElements[currentIndex - 1].focus()
        }
      }
    }
  }

  return suppressEvent
}

export default suppressKeyboardEvent
