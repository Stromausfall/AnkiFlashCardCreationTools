from ankiflashcardcreationtools.CrawlTools import ContentRetrieverUsingSelenium,\
    mergeStringContent
from ankiflashcardcreationtools.CardTools import createSanitizedCard,\
    createCSVFile


if __name__ == '__main__':
    print("Make sure Firefox is running !")
    
    cards = []
    timeout = 1.5
    baseUrl = 'https://docs.python.org/3/tutorial/'
    startUrl = baseUrl + 'index.html'
    cardCategory = 'Python 3'
    
    browser = ContentRetrieverUsingSelenium(timeout)
    
    try:
        _, content = browser.getContentOfPage(startUrl)
        tocTree = content.find('div', { 'class':'toctree-wrapper' })
        links = tocTree.find_all('a', { 'class':'reference internal' })

        for link in links:
            cardTitle = mergeStringContent(link)
            cardLink = baseUrl + link.attrs['href']
            card = createSanitizedCard(cardCategory, cardTitle, cardLink)
            cards.append(card)
    finally:
        browser.close()
    
    print("finished collecting " + str(len(cards)))
    createCSVFile("python3", cards)
