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

function opravaSlov(slovo) {
  const hledaniSlova = document.getBody().findText(slovo)
  Logger.log(hledaniSlova)
  if (hledaniSlova !== null) {
    const naOpraveni = hledaniSlova.getElement().asText()
    const zacatekSlova = hledaniSlova.getStartOffset()
    const konecSlova = hledaniSlova.getEndOffsetInclusive()
    naOpraveni.setBackgroundColor(zacatekSlova, konecSlova, "#FF0000")
}}