# -*- coding: utf-8 -*-

from lxml import html
import requests
import csv
import time



class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print "Elapsed time: {:.3f} sec".format(time.time() - self._startTime)


with Profiler() as p:

    #take verbs
    #amount of some verbs: o - 400+ words, p - 593 words, r - 249, s - 353, u-z - 1430;
    list_of_words = []
    alphabet = ['a/', 'b/', 'c/', 'd/', 'e/', 'f/', 'g/', 'h/', 'i/', 'j/', 'k/', 'l/', 'ł/', 'm/', 'n/', 'o/', 'p/',
                'r/', 's/', 't/', 'u/', 'w/', 'y/', 'z/']
    link = 'http://pl.bab.la/koniugacja/polski/'
    for alphabet_letter in alphabet:
        page = requests.get(link + alphabet_letter)
        tree = html.fromstring(page.content)
        number_of_links_inside_the_page = tree.xpath("""count(//div[@class='toc-links']/ul/li)""")
        for i in range(1, (int(number_of_links_inside_the_page)+1) ):
            url = link + alphabet_letter + `i`
            page2 = requests.get(url)
            tree2 = html.fromstring(page2.content)
            temp_list = tree2.xpath("""//div[@class='content']//div[@class='dict-select-column']/ul/li/a/text()""")
            list_of_words.extend(temp_list)


    #take all forms of all verbs from the web site
    all_forms_and_verbs = []
    for word in list_of_words:
        verb_and_its_forms = []
        verb_and_its_forms.append(word.encode('utf-8'))
        page = requests.get(link + word)
        tree = html.fromstring(page.content)
        forms_of_verb = tree.xpath("""//div[@id='conjFull']//div[@class='conj-tense-block'][1]//div[@class='conj-result']
        /text()""")
        for form in forms_of_verb:
            verb_and_its_forms.append(form.encode('utf-8'))
        all_forms_and_verbs.append(verb_and_its_forms)

    #==========================================================

    # #Write to the file
    #
    # with open("output.csv", 'ab') as resultFile:
    #     writer = csv.writer(resultFile)
    #     writer.writerows(all_forms_and_verbs)


    # #Read from the file

    # with open("verbs_and_forms.csv", 'rb') as resultFile:
    #     reader = csv.reader(resultFile)
    #     for row in reader:
    #         print ', '.join(row)
    #
    #     #Take one certain row and print 1st element in row
    #     interestingrow = [row for idx, row in enumerate(reader) if idx == 4126]
    #     print interestingrow[0][0]
    #
    #     #Take rows in range (a1, a2)
    #     interestingrows = [row for idx, row in enumerate(reader) if idx in (a1, a2)]
