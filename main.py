# -*- coding: utf-8 -*-

import sys
import urllib2
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw


def about():
    print """
            Author      : Steven Aubertin
            File        : {0}
            Description : Display a colored timeline of the Quebec government politics
                          This is base on the data from : http://en.wikipedia.org/wiki/Politics_of_Quebec
            Dependency  : PIL, beautifulsoup4, urllib2

            Copyright Steven Aubertin 2014
        """.format(sys.argv[0])


def parse_int(arg):
    """
        Convert a string to int
        return None if it fails
    """
    try:
        return int(arg)
    except:
        return None


def format_party_years(arg):
    """
        Get an array of year and remove all the None
    """
    out = []
    for i in arg:
        if i:
            out.append(i)
    return out


def format_caption(table):
    """
        Return the String and Years as a tuple
        e.g. ['Elections to the Legislative Assembly of Quebec',  '(1867-1900)']
    """
    years = None
    caption = None

    if table:
        #Get the Caption for the current election
        caption = str(table.find('caption').text)

        #remove the unnecessary information
        caption = caption[:caption.find(' -')]

        #Get the years of those elections
        years = caption[caption.find('('):]

        #Remove the duplicate data
        caption = caption.replace(years, '')

    return [caption, years]


def get_page_web_html(address):
    """
        Query the web page and return the html content
    """
    html = None

    if address:
        response = urllib2.urlopen(address)
        html = response.read()
        response.close()

    return html


def extract_wiki_tables_from_html(html):
    tables = None

    if html:
        soup = BeautifulSoup(html)
        tables = soup.body.findAll('table', attrs={'class': 'wikitable'})

    return tables


def extract_parties_winner_and_there_mandate_count(tables):
    """
        For all the data tables,
        we extract the winner party and the number of mandate count
    """
    winner = []

    for table in tables:
        for tr in table.findAll('tr'):
            is_winner = False
            for td in tr.findAll('td'):
                if td.text == 'Government':
                    is_winner = True
                elif is_winner:
                    succesive_mandate_count = parse_int(td.get('colspan'))
                    winner.append([td.text, 1 if succesive_mandate_count is None else succesive_mandate_count])

    return winner


def extract_all_parties(tables):
    """
    """
    parties = {}

    for table in tables:
        for tr in table.findAll('tr'):
            for td in tr.findAll('td'):
                if td.text == 'Government':
                    continue
                else:
                    entry = td.findAll('b')
                    if entry:
                        parties[td.text] = td.get('bgcolor')
    return parties


def extract_elections_years(tables):
    years = []

    for table in tables:
        table_years = format_party_years([parse_int(y.text) for y in table.findAll('th')])
        for i in table_years:
            years.append(i)

    return years

def main(argv):
    #First we get the data from the web page
    html = get_page_web_html('http://en.wikipedia.org/wiki/Politics_of_Quebec')

    #Then we take what we want
    tables = extract_wiki_tables_from_html(html)

    parties = extract_all_parties(tables)
    print parties

    winners = extract_parties_winner_and_there_mandate_count(tables)
    print winners

    years = extract_elections_years(tables)
    print years

    width = 15
    imgX, imgY = (len(years) * width, 480)
    im = Image.new('RGBA', (imgX, imgY), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    cursor = 0
    for w in winners:
        for i in range(w[1]):
            draw.line((cursor, 0, cursor, imgY), fill=parties[w[0]], width=width)
            cursor += width

    im.show()
    im.save("timeline.ppm")

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
