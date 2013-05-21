#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from collections import defaultdict
import os
os.environ['PYWIKIBOT2_DIR'] = '/home/kleinm/workspace/WikidataVIAFbot_branch'
import pywikibot
import json
en_wikipedia = pywikibot.Site('en', 'wikipedia')
wikidata = en_wikipedia.data_repository()

#from Denny's language codes once at  https://dl.dropboxusercontent.com/u/172199972/wikipedias.txt
lc = file('languageCodes.txt', 'r')
langcodes = lc.readlines()


#this is going to be our matrix
langmatrix = list()
augmentedlangcodes = defaultdict(dict)

#this is the ordering or index of hte matrix
orderedlanglist = list()
orderedshortcodes = list()
for line in langcodes:
    if not line.startswith('#'):
        wikipediaitem, shortcode, languageitem = line.split()
        orderedlanglist.append(languageitem)
        orderedshortcodes.append(shortcode)
        #print languageitem

print orderedlanglist

for lang in orderedlanglist:
    page = pywikibot.ItemPage(wikidata, lang)
    labels = page.get()['labels']
    augmentedlangcodes[lang] = labels

langlinedict = defaultdict(str)
for lang,labels in augmentedlangcodes.iteritems():
    langline = ''
    for orderedshortcode in orderedshortcodes:
        try:
            name = labels[orderedshortcode]
        except KeyError:
            name = 'N/A'
        langline += (name + ' ')
    langlinedict[lang] = langline

print langlinedict

alc = file('augmentedLanguageCodes.txt', 'w')

for line in langcodes:
    if not line.startswith('#'):
        wikipediaitem, shortcode, languageitem = line.split()
        matrixline = langlinedict[languageitem]
        newline = line + matrixline + '\n'
        alc.write(newline)
    else:
        alc.write(line)



