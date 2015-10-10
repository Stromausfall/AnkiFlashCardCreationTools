from ankiflashcardcreationtools.Card import Card
from ankiflashcardcreationtools.CardTools import createCSVFile,\
    createSanitizedCard
from bs4.element import NavigableString
from ankiflashcardcreationtools.CrawlTools import ContentRetrieverUsingSelenium,\
    getUniqueContentInEnvironment

def getTourURLs(browser):
    tourBaseUrl = 'http://tour.golang.org'
    tourStartUrl = tourBaseUrl + '/list'
    _, content = browser.getContentOfPage(tourStartUrl)
    tourUrls = []
    
    for linkEnvironment in content.findAll("a"):
        if 'class' in linkEnvironment.attrs:
            if 'lesson-title' in linkEnvironment.attrs['class']:
                tourUrls.append(tourBaseUrl + linkEnvironment.attrs['href'])
    
    return tourUrls

def addTourCards(cards, browser):
    urls = getTourURLs(browser)
    environmentTag = 'h2'
    cardCategory = 'A Tour of Go'
    
    for startUrl in urls:
        print("looking in " + startUrl)
        currentUrl = startUrl
        index = 1
            
        while True:
            # create the url we want to check
            currentUrl = startUrl + "/" + str(index)
            actualUrl, content = browser.getContentOfPage(currentUrl)
                
            if not startUrl in actualUrl:
                # we already reached the end !
                break
                
            cardTitle = getUniqueContentInEnvironment(content, environmentTag)
            card = createSanitizedCard(cardCategory, cardTitle, actualUrl)
            cards.append(card)
            print("finished Tour card #" + str(index))
            index += 1    

def createGeneralCards(cards, browser, environmentTags, url, cardCategory):
    _, content = browser.getContentOfPage(url)
    preSize = len(cards)
    
    environments = content.findAll(environmentTags)
    for environment in environments:
        if 'id' in environment.attrs:
            linkId = environment.attrs['id']
            cardLink = url + '#' + linkId
            
            cardTitle = ''
            for content in environment.contents:
                if isinstance(content, NavigableString):
                    cardTitle = cardTitle + content 
            
            card = createSanitizedCard(cardCategory, cardTitle, cardLink)
            cards.append(card)
            
    postSize = len(cards)
    print("added " + str(postSize - preSize) + " cards for category : " + cardCategory)

if __name__ == '__main__':
    print("Make sure Firefox is running !")

    cards = []
    # the timeout argument in the constructor may have to be increased - if errors occur
    timeout = 1
    browser = ContentRetrieverUsingSelenium(timeout)
    
    try:
        createGeneralCards(cards, browser, ['h3', 'h2'], 'https://golang.org/doc/install', 'Getting Started')
        addTourCards(cards, browser)
        createGeneralCards(cards, browser, ['h3', 'h2'], 'https://golang.org/ref/mem', 'The Go Memory Model')
        createGeneralCards(cards, browser, ['h3', 'h2'], 'https://golang.org/doc/code.html', 'How to Write Go Code')
        createGeneralCards(cards, browser, ['h3', 'h2'], 'https://golang.org/doc/effective_go.html', 'Effective Go')
        createGeneralCards(cards, browser, ['h3', 'h2'], 'https://golang.org/doc/faq', 'Frequently Asked Questions')
    
    finally:
        browser.close()
        
    createCSVFile("cards", cards)
