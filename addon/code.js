
function onOpen(e) {
  DocumentApp.getUi().createAddonMenu()
      .addItem('Start', 'showSidebar')
      .addToUi()
}
function onInstall(e) {
  onOpen(e)
}
function showSidebar() {
  const html = HtmlService.createTemplateFromFile('sidebar').evaluate().setTitle("Slohobot")
  DocumentApp.getUi()
    .showSidebar(html)
}

const document = DocumentApp.getActiveDocument()
const body = document.getBody()

function extractTextForServer() {
  return document.getBody().getText()
}

function extractTextFromParagraphs() {
  const paragraphs = document.getBody().getParagraphs()
  const paragraphsText = paragraphs.map( p => {return p.getText()})
  return paragraphsText
}

function wordCorrection(word) {
  let wordSearch = document.getBody().findText(word.original)
  while (wordSearch !== null) {
    let forCorrection = wordSearch.getElement().asText()
    let start = wordSearch.getStartOffset()
    let end = wordSearch.getEndOffsetInclusive()
    forCorrection.setStrikethrough(start, end, true)
    forCorrection.insertText(end + 1, " " + word.correction)
    const correctedWordLength = end + word.correction.length
    forCorrection.setStrikethrough(end + 1, correctedWordLength + 1, false)
    wordSearch = body.findText(word.original, wordSearch)
  }
  let wordSearch1 = document.getBody().findText(word.original)
  while (wordSearch1 !== null) {
    let forCorrection = wordSearch1.getElement().asText()
    let start = wordSearch1.getStartOffset()
    forCorrection.insertText(start, "*")
    wordSearch1 = body.findText(word.original, wordSearch1)
  }
}

function deleteWords() {
  body.replaceText("(?:^|\\s+)\\*\\S+", "")
}

function markRepetition(regex) {
  let repeatedWord = body.findText(regex)
  while (repeatedWord !== null) {
    let element = repeatedWord.getElement().asText()
    let start = repeatedWord.getStartOffset()
    let end = repeatedWord.getEndOffsetInclusive()
    element.setBackgroundColor(start, end, "#FF0000")
    repeatedWord = body.findText(regex, repeatedWord)
  }
}
