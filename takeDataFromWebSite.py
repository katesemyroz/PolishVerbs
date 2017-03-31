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


list_of_words = []
all_forms_and_verbs = []
translations = []
link = 'http://pl.bab.la/koniugacja/polski/'


def take_all_verbs():
    #amount of some verbs: o - 400+ words, p - 593 words, r - 249, s - 353, u-z - 1430;
    alphabet = ['a/', 'b/', 'c/', 'd/', 'e/', 'f/', 'g/', 'h/', 'i/', 'j/', 'k/', 'l/', 'ł/', 'm/', 'n/', 'o/', 'p/',
                'r/', 's/', 't/', 'u/', 'w/', 'y/', 'z/']
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

def take_all_forms_of_all_verbs():
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

def take_russian_translation_of_verbs():
    all_verbs = []
    with open("verbs_and_forms.csv", 'rb') as resultFile:
        reader = csv.reader(resultFile)
        for row in reader:
            all_verbs.append(row[0])

    url = "http://pl.bab.la/slownik/polski-rosyjski/"
    #for word in all_verbs:
    for x in range(4660, 4663):
        one_verb_and_translation = []
        print all_verbs[x], type(all_verbs[x])
        one_verb_and_translation.append(all_verbs[x])
        page = requests.get(url + all_verbs[x])
        tree = html.fromstring(page.content)
        translations_of_one_verb_list = tree.xpath("""//div[@class='content'][1]//
        div[@class='quick-result-entry']//ul[@class='sense-group-results']/li/a/text()""")

        #print len(translations_of_one_verb_list)
        if len(translations_of_one_verb_list) != 0:
            temp_list = []
            for tr in translations_of_one_verb_list:
                temp_list.append(tr.encode("utf-8"))
            translations_of_one_verb_str = '\n'.join(temp_list)
            one_verb_and_translation.append(translations_of_one_verb_str)
        translations.append(one_verb_and_translation)

    with open("translations.csv", 'ab') as resultFile:
        writer = csv.writer(resultFile)
        writer.writerows(translations)



def write_to_the_file(filename):
    with open("verbs_and_forms.csv", 'ab') as resultFile:
        writer = csv.writer(resultFile)
        writer.writerows(filename)

def read_from_the_file_and_print_all_data(file_name):
    with open(file_name, 'rb') as resultFile:
        reader = csv.reader(resultFile)
        for row in reader:
            print ', '.join(row)

def print_1st_el_in_row():
    #Take one certain row and print 1st element in row 4126
    with open("verbs_and_forms.csv", 'rb') as resultFile:
        reader = csv.reader(resultFile)
        interestingrow = [row for idx, row in enumerate(reader) if idx == 4126]
        print interestingrow[0][0]

def take_rows_in_range_a1_a2(a1, a2):
    with open("verbs_and_forms.csv", 'rb') as resultFile:
        reader = csv.reader(resultFile)
        interestingrows = [row for idx, row in enumerate(reader) if idx in (a1, a2)]
        print interestingrows


with Profiler() as p:
    take_russian_translation_of_verbs()
    read_from_the_file_and_print_all_data("translations.csv")






