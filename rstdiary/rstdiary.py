import os
import sys
import functools

import argparse

from collections import defaultdict

import docutils
from docutils.frontend import OptionParser
from docutils.utils import new_document
from docutils.parsers.rst import Parser
from docutils.writers.html4css1 import HTMLTranslator

from jinja2 import Environment, PackageLoader

import logging

import ConfigParser

import re

from datetime import datetime

all_months = set()
# a dict that keeps entries keyed by month.
# later, we can walk each key kept in all_months
# to build the pages
all_entries = defaultdict(list)


class Entry():

    def __init__(self, date, body):
        self.date = date
        self.body = body
        # mangle the header to be a bit more readable
        self.body = re.sub(r"<h1>.*</h1>",
                           r'<h2>%s <small>%s</small></h2>' %
                           (date.strftime("%d"),
                            date.strftime("%A")), body)
        self.month = "%4d-%02d" % (date.year,
                                   date.month)
        # set to 0 if this is an entry for a monday
        self.start_of_week = True if self.date.weekday() == 0 else False
        # used to set a <a> anchor for each entry
        self.anchor = "%4d-%02d-%02d" % (date.year, date.month, date.day)

    def __repr__(self):
        return str(self.date)


def parse_entries(input_file):
    global all_months, all_entries

    file = open(input_file)
    try:
        text = file.read()
    finally:
        file.close()

    parser = Parser()
    settings = OptionParser(
        components=(Parser,
                    docutils.writers.html4css1.Writer)).get_default_values()
    docroot = docutils.utils.new_document(file.name, settings)
    parser.parse(text, docroot)

    for i in docroot.traverse(condition=docutils.nodes.section):
        try:
            date_string = re.findall(r'(\d{4}-\d{1,2}-\d{1,2})',
                                     str(i.children[0]))[0]
            logging.debug("Found entry : %s" % date_string)
            date = datetime.strptime(date_string, "%Y-%m-%d")
        except IndexError:
            sys.stderr.write("can not parse section : %s\n" %
                             str(i.children[0]))
            sys.exit(1)

        translator = HTMLTranslator(docroot)
        i.walkabout(translator)
        body = ''.join(translator.body)

        entry = Entry(date, body)

        all_months.add(entry.month)
        all_entries[entry.month].append(entry)

    all_months = sorted(all_months, reverse=True)


def write_html(config):
    env = Environment(loader=PackageLoader('rstdiary', 'templates'))
    template = env.get_template('page.html')

    output_dir = config.get('rstdiary', 'output_dir')

    if not os.path.isdir(output_dir):
        sys.stderr.write("output_dir <%s> : not a directory\n" % output_dir)
        sys.exit(1)

    first = True
    for month in all_months:

        month_entries = all_entries[month]
        month_entries.sort(key=lambda e: e.date, reverse=True)

        string_month = datetime.strptime(month, "%Y-%m").strftime("%B %Y")

        output = template.render(title=config.get('rstdiary', 'title'),
                                 about=config.get('rstdiary', 'about'),
                                 month=string_month,
                                 all_months=all_months,
                                 month_entries=month_entries)

        filename = os.path.join(output_dir, '%s.html' % month)

        if first:
            index_html = os.path.join(output_dir, 'index.html')
            if os.path.exists(index_html):
                # everything overwrites by design
                logging.debug("Removing existing index.html")
                os.unlink(index_html)
            os.symlink('%s.html' % month,
                       os.path.join(output_dir, 'index.html'))
            first = False

        logging.debug("Writing %s" % filename)
        with open(filename, 'w') as f:
            f.write(output)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a simple HTML diary")
    parser.add_argument('-c', '--config', help="Path to config file",
                        required=True)
    parser.add_argument('-d', '--debug', action='store_true')

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Debugging enabled")

    config = ConfigParser.RawConfigParser()
    config.read(args.config)

    input_filename = config.get('rstdiary', 'input')
    logging.debug("input_filename = %s" % input_filename)

    parse_entries(input_filename)
    write_html(config)

if __name__ == "__main__":
    main()
