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
  const hledaniSlova = document.getBody().findText(slovo.original)
  if (hledaniSlova !== null) {
    naOpraveni = hledaniSlova.getElement().asText()
    zacatekSlova = hledaniSlova.getStartOffset()
    konecSlova = hledaniSlova.getEndOffsetInclusive()
    naOpraveni.setStrikethrough(zacatekSlova, konecSlova, true)
    naOpraveni.insertText(konecSlova + 1, slovo.oprava)
    const delkaOpravenehoSlova = konecSlova + slovo.oprava.length
    naOpraveni.setStrikethrough(konecSlova + 1, delkaOpravenehoSlova, false)
  naOpraveni = hledaniSlova.getElement().asText()
  

}}

function smazaniSlov() {
  console.log("1")
  const paragraphs = document.getBody().getParagraphs()
  paragraphs.forEach(paragraph => {
    const textNaEdit = paragraph.editAsText()
    const text = textNaEdit.getText()
    for (let i = text.length - 1; i >= 0; i --) {
      const attributes = textNaEdit.getAttributes(i)
      console.log(i)
      if(attributes[DocumentApp.Attribute.STRIKETHROUGH]) {
        console.log("bruh")
        textNaEdit.deleteText(i, i)
      }
    }
  })
}

