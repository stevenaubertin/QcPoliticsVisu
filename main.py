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


class Election:
    """
        Class that contain information about an election

        members:
            String caption : a caption string of what this election is about
            int year_from  : an integer about the starting year of the election mandate
            int year_to    : an integer about the ending year of the election mandate
            list parties   : a list of parties in that election
            dict winners   : a dictionary of parties winners as {year: winner}
    """
    def __set_caption(self, caption):
        assert caption and isinstance(caption, str)
        self.caption = caption

    def __set_years_bound(self, year_from, year_to):
        assert isinstance(year_from, int) and isinstance(year_to, int)
        self.year_from = parse_int(year_from)
        self.year_to = parse_int(year_to)

    def __set_parties(self, parties):
        assert parties and isinstance(parties, list)
        self.parties = parties

    def __set_winners(self, winners):
        assert winners and isinstance(winners, dict)
        self.winners = winners

    def __init__(self, caption, year_from, year_to, parties, winners):
        self.caption = None
        self.__set_caption(caption)

        self.year_from = None
        self.year_to = None
        self.__set_years_bound(year_from, year_to)

        self.parties = None
        self.__set_parties(parties)

        self.winners = None
        self.__set_winners(winners)

    def __str__(self):
        return "{0} ( {1} - {2} )".format(self.caption, self.year_from, self.year_to)


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


    input()

    #Container this should be a class
    dataTable = {}

    #list of parties colors
    colors = {}
    winners = []



    for table in tables:
        """
            list of the winners party followed by is consecutive mandate, arrange by [winner_party_name, consecutive_mandate]
            e.i. [[u'Conservative', 3], [u'Liberal', 1], [u'Conservative', 1], [u'Liberal', 2], [u'Conservative', 1], [u'Liberal', 2]]
        """
        elections = []
        winner = []

        #This is the number of seats of a particular party
        dataRow = {}

        #Description of the table being read
        caption, years = format_caption(table)

        #List of years of this table


        winners = extract_parties_winner_and_there_mandate_count(tables)

        #Table body (the table itself)
        #For all row in the table
        for tr in table.findAll('tr'):
            #True if we are fetching the table row about winner of elections
            isWinner = False
            lastEntry = None

            #For all table data
            for td in tr.findAll('td'):
                if td.text == 'Government':
                    isWinner = True
                elif isWinner:
                    succesive_mandate_count = parse_int(td.get('colspan'))
                    winner.append([td.text, 1 if succesive_mandate_count is None else succesive_mandate_count])

                    #color that represent the party
                    colors[td.text] = td.get('bgcolor')
                else:
                    entry = td.findAll('b')
                    if entry:
                        #Add array for data, this data's gonna be the number of seats for all the parties
                        dataRow[td.text] = []
                        lastEntry = td.text

                        #color that represent the party
                        colors[td.text] = td.get('bgcolor')
<<<<<<< HEAD
                    else:
                        entry = td.findAll('b')
                        if entry:
                            #Add array for data, this data's gonna be the number of seats for all the parties
                            dataRow[td.text] = []
                            lastEntry = td.text

                            #color that represent the party
                            colors[td.text] = td.get('bgcolor')
                        elif lastEntry:
                            #add seats value
                            dataRow[lastEntry].append(td.text if td.text else '0')
=======
                    elif lastEntry:
                        dataRow[lastEntry].append(td.text if td.text else '0')
>>>>>>> FETCH_HEAD

        winners.append([winner, part_years])
        dataTable[caption] = [winner, part_years, dataRow]

    print dataTable

    #Here there is some work to clean it up
    print
    for i in dataTable:
        print
        caption = i
        years = []
        winner = []
        count = 2 # winner and years
        for j in dataTable[i]:
            if count == 0:#row data
                break
            elif count == 1:#years
                for l in j:
                    years.append(l)
            else:#winners
                for l in j:
                    winner.append(l)
            count -= 1
        ez = []
        for party, count in winner:
            for i in range(count):
                ez.append(party.encode('ascii'))
        winner = ez

        imgX, imgY = (720, 405)
        im = Image.new('RGBA', (imgX, imgY), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)

        i = 0
        j = 0
        for w in winner:
            proportion = (imgX / len(winner))
            color = colors[w]
            draw.line((i, 0, i, imgY), fill=color, width=proportion)
            draw.text((i, 0), years[j].__str__(), fill=(255,255,255))
            j += 1
            i += proportion
        im.show()
        im.save(caption + ".ppm")
        print

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
