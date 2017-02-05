
// actions creators
export function setDocumentTitle(title) {
  let title_root = 'PinPict'
  if (title) {
    document.title = `${title} - ${title_root}`
  } else {
    document.title = `${title_root}`
  }
}
