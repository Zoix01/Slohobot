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
function extractTextFromParagraphs() {
  const paragraphs = document.getBody().getParagraphs()
  const paragraphsText = paragraphs.map( p => {return p.getText()})
  return paragraphsText
}

function extractTextForServer() {
  return document.getBody().getText()
}

function opravaSlov(slovo) {
  var hledaniSlova = document.getBody().findText(slovo)
  Logger.log(hledaniSlova)
  if (hledaniSlova !== null) {
    var naOpraveni = hledaniSlova.getElement().asText()
    var zacatekSlova = hledaniSlova.getStartOffset()
    var konecSlova = hledaniSlova.getEndOffsetInclusive()
    naOpraveni.setBackgroundColor(zacatekSlova, konecSlova, "#FFFF00")
  }
}