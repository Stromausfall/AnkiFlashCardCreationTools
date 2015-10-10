import csv
from ankiflashcardcreationtools.Card import Card
from csv import excel_tab

def createCSVFile(fileName, cards):
    with open(fileName + '.csv', 'wt', encoding='utf8') as csvFile:
        csvFileWriter = csv.writer(csvFile, dialect=excel_tab)
        
        for card in cards:
            frontOfCard = '<h5> <font color="888888">' + card.category + '</font></h5><center><h3>' + card.title + '</h3></center>'
            backOfCard = '<center><h4><a href="' + card.link + '">' + card.title + '</a></h4></center>'
        
            csvFileWriter.writerow([frontOfCard, backOfCard])

def _sanitizeValue(value):
    value = value.replace("\n", " ")
    value = value.replace("\t", "    ")
    return value

def createSanitizedCard(cardCategory, cardTitle, cardLink):
    cardCategory = _sanitizeValue(cardCategory)
    cardTitle = _sanitizeValue(cardTitle)
    cardLink = _sanitizeValue(cardLink)

    return Card(cardCategory, cardTitle, cardLink)
