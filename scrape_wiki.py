#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 14:36:47 2017

@author: stephendove
"""

import csv
import requests
from BeautifulSoup import BeautifulSoup

# Printing Instructions - i.e. where to write the .csv to
def printInstr():
    filename = raw_input("Enter the filename (no extension): ")
    filename += ".csv"
    outfile = open(filename, "wb")
    writer = csv.writer(outfile)
    return writer,outfile

# Return the formatted HTML as a BeautifulSoup object
def formatHTML(url,element,attrType,attrName):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    table = soup.find(element, attrs={attrType: attrName})
    return table,soup

# Return genres in an appopriate format
def genreParser(tag):
    intoGenres = tag.find('div', attrs={'class': 'hlist'})
    try:
        genreTable = intoGenres.findAll('li')
    except AttributeError: 
        genres = tag.td.text
    else:
        genresTmp = ''
        for li in genreTable:
            genres += li.text + ';'
        genres = genresTmp[0:(len(genresTmp)-1)]
    return genres


writer,outfile = printInstr()
print "Thanks, I'm working on it!"

url = 'https://en.wikipedia.org/wiki/Lists_of_musicians'
table,_ = formatHTML(url,'div','class','mw-parser-output')

allUrls = []
for cell in table.findAll('a'):
    exten = cell['href']
    if exten[0:7] == '/wiki/L':
        allUrls.append(exten)
        if exten == '/wiki/List_of_West_Coast_hip_hop_artists':
            break

bandUrls = []
count = 0
for url in allUrls:
    count += 1
    table,_ = formatHTML('https://en.wikipedia.org'+url,'div','class','mw-parser-output')
    for cell in table.findAll('a'):
        try:
            exten = cell['href']
        except KeyError:
            continue
        if exten[0:6] == '/wiki/' and not bandUrls.__contains__(exten):
            bandUrls.append(exten)
    if count == 10:
        break

    #break


for url in bandUrls:
    table,soup = formatHTML('https://en.wikipedia.org'+url,'table','class','infobox vcard plainlist')
    if table == None:
        continue
    #print "HERE"
    bandInfo = []
    done = 0
    for cell in table.findAll('tr'):
        try:
            thTitle = cell.th.text
        except AttributeError:
            continue
        if thTitle == 'Origin':
            head = soup.find('h1', attrs={'id': 'firstHeading'})
            bandInfo.append(head.text)
            bandInfo.append(cell.findAll('td')[0].text)
            done += 1
            if done == 2:
                break
        if thTitle == 'Genres':
            genres = genreParser(cell)
            done += 1
            if done == 2:
                break
    if done > 1:
        bandInfo.append(genres)
        
    if len(bandInfo) > 0:
        try :
            print head.text
            writer.writerows([bandInfo])
        except UnicodeEncodeError:
            continue
    
outfile.close()


