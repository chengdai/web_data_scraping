import requests
from bs4 import BeautifulSoup

def extractBloombergHeadlines():
    '''Scrapes the headlines from the homepage Bloomberg.com and returns all headlines. 

        :param: none
        :returns: list as strings of headlines
    '''

    url = "http://www.bloomberg.com/"
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    attributeA = soup.find_all('a')
    headlines = []

    for a in attributeA:
        if u'data-resource-type' in a.attrs and 'article' in a[u'data-resource-type'] and 'headline' in str(a['class']):
            headlines.append(a.text.encode('ascii','ignore').strip())
    return headlines

def extractNYTimesHeadlines():
    '''Scrapes the headlines from the homepage NYTimes.com and returns all headlines. 

        :param: none
        :returns: list as strings of headlines
    '''

    url = "http://www.nytimes.com/"
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    attributeA = soup.find_all('h1') + soup.find_all('h2') + soup.find_all('h3')
    headlines = []

    for a in attributeA:
        if 'story-heading' in str(a['class']):
            headlines.append(a.text.encode('ascii','ignore').strip())
    return headlines

def extractGoogleNewsHeadlines():
    '''Scrapes the headlines from the Google News homepage (headline view) and returns all headlines. 

        :param: none
        :returns: list as strings of headlines
    '''

    url = "https://news.google.com/?sdm=HEADLINE&authuser=0"
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    attributeA = soup.find_all('span', { "class" : "titletext" })
    headlines = []

    for a in attributeA:
        if 'titletext' in str(a['class']):
            headlines.append(a.text.encode('ascii','ignore').strip())
    return headlines



def searchHeadlines(search_words):
    '''Aggregates all headlines from the homepage of various news sites and extract headlines 
    containing the user requested search words

        :param: a list of strings or a string of keyword(s)
        :returns: list as strings of headlines that match the keyword(s)
    '''

    headlines = extractBloombergHeadlines() + extractNYTimesHeadlines() + extractGoogleNewsHeadlines()

    relevant = []

    if type(search_words) == str:
        for headline in headlines:
            if search_words in headline:
                relevant.append(headline)
    if type(search_words) == list:
        for headline in headlines:
            for keyword in search_words:
                if keyword in headline:
                    relevant.append(headline)

    return relevant

