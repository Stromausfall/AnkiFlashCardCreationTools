import csv

def createCSVFile(fileName, cards):
    with open(fileName + '.csv', 'wt', encoding='utf8') as csvFile:
        csvFileWriter = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
        
        for card in cards:
            frontOfCard = '<h5> <font color="888888">' + card.category + '</font></h5><center><h3>' + card.title + '</h3></center>'
            backOfCard = '<center><h4><a href="' + card.link + '">' + card.title + '</a></h4></center>'
        
            csvFileWriter.writerow([frontOfCard, backOfCard])
