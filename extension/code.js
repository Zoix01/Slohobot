function onOpen(e) {
  DocumentApp.getUi().createAddonMenu()
      .addItem('Start', 'showSidebar')
      .addToUi();
}
function onInstall(e) {
  onOpen(e);
}
function showSidebar() {
  const html = HtmlService.createTemplateFromFile('sidebar').evaluate().setTitle("Slohobot")
  DocumentApp.getUi()
    .showSidebar(html)
}
const document = DocumentApp.getActiveDocument()
const body = document.getBody()

function extractTextFromParagraphs() {
  const paragraphs = document.getBody().getParagraphs()
  const paragraphsText = paragraphs.map( p => {return p.getText()})
  return paragraphsText
}

function extractTextForServer() {
  return document.getBody().getText()
}

let naOpraveni = null
let zacatekSlova = null
let konecSlova = null

function opravaSlov(slovo) {
  let hledaniSlova = document.getBody().findText(slovo.original)
  if (hledaniSlova !== null) {
    naOpraveni = hledaniSlova.getElement().asText()
    zacatekSlova = hledaniSlova.getStartOffset()
    konecSlova = hledaniSlova.getEndOffsetInclusive()
    naOpraveni.setStrikethrough(zacatekSlova, konecSlova, true)
    naOpraveni.insertText(konecSlova + 1, " " + slovo.oprava)
    const delkaOpravenehoSlova = konecSlova + slovo.oprava.length
    naOpraveni.setStrikethrough(konecSlova + 1, delkaOpravenehoSlova + 1, false)
  }
  hledaniSlova = document.getBody().findText(slovo.original)
  naOpraveni = hledaniSlova.getElement().asText()
  zacatekSlova = hledaniSlova.getStartOffset()
  naOpraveni.insertText(zacatekSlova, "*")
}

function smazaniSlov() {
  body.replaceText("\\s+\\*\\S+", "")
}

