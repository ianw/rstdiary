import sys
import os
import docutils

from docutils.frontend import OptionParser
from docutils.utils import new_document
from docutils.parsers.rst import Parser
from docutils.writers.html4css1 import HTMLTranslator

import re
import datetime

file = open('./test.rst')

try:
    text = file.read()
finally:
    file.close()

parser = Parser()
settings = OptionParser(
    components=(Parser,docutils.writers.html4css1.Writer)).get_default_values()
docroot = docutils.utils.new_document(file.name,settings)
parser.parse(text, docroot)

entries = []

for i in docroot.traverse(condition=docutils.nodes.section):

    date_string = re.findall(r'(\d{4}-\d{1,2}-\d{1,2})', str(i.children[0]))[0]
    if date_string:
        date=datetime.datetime.strptime(date_string, "%Y-%m-%d")

    translator = HTMLTranslator(docroot)
    i.walkabout(translator)
    body = ''.join(translator.body)

    entry = {
        'date' : date,
        'body' : body
    }

    entries.append(entry)

entries.sort(key=lambda k: k['date'], reverse=True)

# make a list of all months for the sidebar page
cur_month = "%4d-%02d" % (entries[0]['date'].year,
                          entries[0]['date'].month)
all_months = [cur_month]
for e in entries:
    e_month = "%4d-%02d" % (e['date'].year,
                            e['date'].month)
    if e_month != cur_month:
        cur_month = e_month
        all_months.append(cur_month)


# go through each entry and write it out to a page.  First page is
# index.html, then each month's entries gets it's own "YYYY-MM.html"
# page
cur_month = "%4d-%02d" % (entries[0]['date'].year,
                          entries[0]['date'].month)
output = open('./index.html', 'w')

for e in entries:
    e_month = "%4d-%02d" % (e['date'].year,
                            e['date'].month)
    if e_month != cur_month:
        cur_month = e_month
        output.close()
        output = open('./%s.html' % cur_month, 'w')

    output.write(e['body'])


