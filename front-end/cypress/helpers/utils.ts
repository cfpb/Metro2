export const stripHtmlTags = (htmlString: string) => {
  const div = document.createElement('div')
  div.innerHTML = htmlString
  return div.textContent
}
