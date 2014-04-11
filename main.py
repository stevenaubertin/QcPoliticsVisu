# -*- coding: utf-8 -*-

import sys
import urllib2
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw

def about():
    print """
            Author      : Steven Aubertin
            File        : {0}
            Description : Display a color timeline of the Quebec government politics
                          base on the data from : http://en.wikipedia.org/wiki/Politics_of_Quebec

            Copyright Steven Aubertin 2014
        """.format(sys.argv[0])


def parse_int(arg):
    try:
        return int(arg)
    except:
        return None

def format_party_years(arg):
    out = []
    for i in arg:
        if i:
            out.append(i)
    return out


def main(argv):
    #Get the web page data
    response = urllib2.urlopen('http://en.wikipedia.org/wiki/Politics_of_Quebec')
    html = response.read()
    response.close()

    #Make it easier to parse
    soup = BeautifulSoup(html)
    tables = soup.body.findAll('table', attrs={'class':'wikitable'})

    #Container this should be a class
    dataTable = {}

    #list of parties colors
    colors = {}

    for table in tables:
        #list of the winners party followed by is consecutive mandate, arrange by [winner_party_name, consecutive_mandate]
        # e.i. [[u'Conservative', 3], [u'Liberal', 1], [u'Conservative', 1], [u'Liberal', 2], [u'Conservative', 1], [u'Liberal', 2]]
        winner = []

        #This is the number of seats of a particular party
        dataRow = {}

        #Description of the table being read
        caption = table.find('caption').text

        #List of years of this table
        part_years = format_party_years([parse_int(y.text) for y in table.findAll('th')])

        #Table body (the table itself)
        for tbody in table.findAll('tbody'):

            #For all row in the table
            for tr in tbody.findAll('tr'):
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
                        elif lastEntry:
                            dataRow[lastEntry].append(td.text if td.text else '0')

        dataTable[caption] = [winner, part_years, dataRow]

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
        proportion = (imgX / len(winner))
        for w in winner:
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






