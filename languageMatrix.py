#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from collections import defaultdict
#import os
#os.environ['PYWIKIBOT2_DIR'] = '/home/notconfusing/workspace/WikidataVIAFbot_branch'
import pywikibot
import json
en_wikipedia = pywikibot.Site('en', 'wikipedia')
wikidata = en_wikipedia.data_repository()

#from Denny's language codes once at  https://dl.dropboxusercontent.com/u/172199972/wikipedias.txt
lc = file('languageCodes.dedupe.txt', 'r')
langcodes = lc.readlines()


#this is going to be our matrix
langmatrix = list()
augmentedlangcodes = defaultdict(dict)
#key languageitem number value shortocde
itemnumshortcodedict = dict()

#this is the ordering or index of hte matrix
orderedlanglist = list()
orderedshortcodes = list()
for line in langcodes:
    if not line.startswith('#'):
        wikipediaitem, shortcode, languageitem = line.split()
        if not languageitem in orderedlanglist:
            orderedlanglist.append(languageitem)
        else:
            print 'earlydupe:', languageitem
        if not shortcode in orderedshortcodes:
            orderedshortcodes.append(shortcode)
        else:
            print 'earlydupe:', shortcode
        itemnumshortcodedict[languageitem] = shortcode
        
        #print languageitem

for lang in orderedlanglist:
    page = pywikibot.ItemPage(wikidata, lang)
    print page
    labels = page.get()['labels']
    augmentedlangcodes[lang] = labels

langlinedict = defaultdict(str)

#for csv
for lang,labels in augmentedlangcodes.iteritems():
    langline = ''
    for orderedshortcode in orderedshortcodes:
        try:
            name = labels[orderedshortcode]
        except KeyError:
            name = 'N/A'
        langline += (name + ' ')
    langlinedict[lang] = langline
    
#write csv for R directly
rd = file('bindata.csv', 'w')
header = ''
for orderedshortcode in orderedshortcodes:
    header += (orderedshortcode + ',')
#remove last comma
header = header[:-1]
#add an new line
header += '\n'
rd.write(header)

for lang in orderedlanglist:
    langlabelsdict = augmentedlangcodes[lang]
    langline = ''
    for osc in orderedshortcodes:
        try:
            name = langlabelsdict[osc]
            bin = '1'
        except KeyError:
            name = 'N/A'
            bin = '0'
        langline += (bin + ',')
    if lang == 'Q1860':
        print langline
    #remove last comma
    langline = langline[:-1]
    #add an new line
    langline += '\n'
    rd.write(langline)


alc = file('augmentedLanguageCodes.txt', 'w')

for line in langcodes:
    if not line.startswith('#'):
        wikipediaitem, shortcode, languageitem = line.split()
        matrixline = langlinedict[languageitem]
        newline = line + matrixline + '\n'
        alc.write(newline)
    else:
        alc.write(line)



