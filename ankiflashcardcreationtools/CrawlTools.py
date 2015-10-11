from selenium.webdriver import Firefox
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from urllib import request  
import time

def getContentUsingUrllib(url):
    htmlContent = request.urlopen(url).read()    
    return BeautifulSoup(htmlContent) 

class ContentRetrieverUsingSelenium:
    def __init__(self, timeout):
        self.browser = Firefox()
        self.timeout = timeout
    
    def getContentOfPage(self, url):
        self.browser.get(url)
        
        time.sleep(self.timeout)
        
        page_source = self.browser.page_source
        page_source = page_source.encode('gbk', 'ignore')
        
        return (self.browser.current_url, BeautifulSoup(page_source))
    
    def close(self):
        self.browser.close()

def mergeStringContent(element):
    value = ''
    for content in element.contents:
        if isinstance(content, NavigableString):
            value = value + content
    
    return value 

def getUniqueContentInEnvironment(content, environmentTag):
    '''
    searches the environment and returns its string content - it is expected
    that only one such environment is inside the content to search in
    '''
    environments = content.findAll(environmentTag)
    environmentsCount = len(environments)
    
    if environmentsCount != 1:
        raise ValueError("expected exactly one '" + environmentTag + "' environment - but found " + str(environmentsCount) + " in " + content)
    
    environment = environments[0]
    # the environment should only contain a string
    for content in environment.children:
        if isinstance(content, NavigableString):
            return content
