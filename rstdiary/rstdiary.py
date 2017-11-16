"""
    rstdiary
    ~~~~~~~~

    A simple rst to static HTML diary generator

    :copyright: (c) 2014 by Ian Wienand.
    :license: MIT, see LICENSE for more details.
"""

import argparse
import codecs
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import logging
import os
import sys
import re

from collections import defaultdict, OrderedDict
from datetime import datetime

import docutils
from docutils.frontend import OptionParser
from docutils.parsers.rst import Parser
from docutils.writers.html4css1 import HTMLTranslator

from jinja2 import Environment, PackageLoader
import locale
#
# globals
#
config = None
locale.setlocale(locale.LC_TIME, '')
# a dict that keeps entries keyed by month.
# later, we can walk each key kept in all_months
# to build the pages
all_entries = defaultdict(list)

# set of keys for all_entries.  sorted by parse_entries into reverse
# date order (i.e. latest month is first)
all_months = set()

# the todo list section
todo = None


class Todo():
    """The todo list"""
    def __init__(self, body_html):
        self.body_html = re.sub(r"<h1>.*</h1>", '', body_html)


class Entry():
    """Representation of a single day's entry in the RST file"""
    def __init__(self, date, body):
        self.date = date
        self.body = body
        # mangle the header to be a bit more readable
        self.body_html = re.sub(r"<h1>.*</h1>",
                                r'<h2>%s <small>%s</small></h2>' %
                                (date.strftime("%d"),
                                 date.strftime("%A")), self.body)
        self.month = "%4d-%02d" % (date.year,
                                   date.month)
        # set to 0 if this is an entry for a monday
        self.start_of_week = True if self.date.weekday() == 0 else False
        # used to set a <a> anchor for each entry
        self.anchor = "%4d-%02d-%02d" % (date.year, date.month, date.day)

    def __repr__(self):
        return str(self.date)


# go through the input_file and pull out each section; parse the date
# and create an Entry() object.  Entries go into all_entries keyed by
# the month it was created in; each month we see gets an entry in
# all_months
def parse_entries(input_file):
    global all_months, all_entries, todo

    file = codecs.open(input_file, 'r', 'utf-8')
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
            if str(i.children[0]) == "<title>todo</title>":
                logging.debug("Found todo section")
                translator = HTMLTranslator(docroot)
                i.walkabout(translator)
                body = ''.join(translator.body)
                todo = Todo(body)
                continue
        except IndexError:
            pass

        try:
            date_string = re.findall(r'(\d{4}-\d{1,2}-\d{1,2})',
                                     str(i.children[0]))[0]
            logging.debug("Found entry: %s" % date_string)
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


# write out the HTML pages via our template
def write_html():
    env = Environment(loader=PackageLoader('rstdiary', 'templates'))
    template = env.get_template('page.html')
    output_dir = config.get('rstdiary', 'output_dir')

    # since this is in order, we can bunch them by year to get
    # an accordian list in the output
    all_months_by_year = OrderedDict()
    for month in all_months:
        y, m = month.split("-")
        all_months_by_year.setdefault(y, []).append(m)

    first = True
    for index, month in enumerate(all_months):
        month_entries = all_entries[month]
        month_entries.sort(key=lambda e: e.date, reverse=True)

        string_month = (datetime.strptime(month, "%Y-%m")
                        .strftime("%B %Y")
                        .decode('utf-8'))

        previous_month = all_months[index - 1] if index >= 1 else None
        next_month = (all_months[index + 1]
                      if index < len(all_months) - 1 else None)

        output = template.render(title=config.get('rstdiary', 'title'),
                                 about=config.get('rstdiary', 'about'),
                                 month=string_month,
                                 all_months_by_year=all_months_by_year,
                                 month_entries=month_entries,
                                 previous_month=previous_month,
                                 next_month=next_month,
                                 todo=todo)

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
        with codecs.open(filename, 'w', 'utf-8') as f:
            f.write(output)


# a simple atom feed of just the latest month
def write_atom():
    env = Environment(loader=PackageLoader('rstdiary', 'templates'))
    template = env.get_template('atom.xml')
    output_dir = config.get('rstdiary', 'output_dir')

    # just write the latest month's entries into the atom feed
    month = all_months[0]
    month_entries = all_entries[month]
    month_entries.sort(key=lambda e: e.date, reverse=True)

    output = template.render(title=config.get('rstdiary', 'title'),
                             site_root=config.get('rstdiary', 'site_root'),
                             author_name=config.get('rstdiary', 'author_name'),
                             month=month,
                             updated=datetime.utcnow().isoformat("T")+"Z",
                             month_entries=month_entries)

    filename = os.path.join(output_dir, 'atom.xml')
    logging.debug("Writing atom feed for %s to %s" % (month, filename))
    with codecs.open(filename, 'w', 'utf-8') as f:
        f.write(output)


def main():
    global config

    parser = argparse.ArgumentParser(
        description="Generate a simple HTML diary")
    parser.add_argument("config", help="Path to config file")
    parser.add_argument('-d', '--debug', action='store_true')

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Debugging enabled")

    config = configparser.RawConfigParser()
    config.read(args.config)

    try:
        # validate required fields
        for check in ['input', 'output_dir', 'title',
                      'author_name', 'site_root']:
            val = config.get('rstdiary', check)
            logging.debug("config: %s=%s" % (check, val))
    except configparser.NoOptionError:
        sys.stderr.write("Config file doesn't contain: %s\n" % check)
        sys.exit(1)
    except configparser.NoSectionError:
        sys.stderr.write("Config file doesn't contain section [rstdiary]\n")
        sys.exit(1)

    output_dir = config.get('rstdiary', 'output_dir')
    if not os.path.isdir(output_dir):
        sys.stderr.write("output_dir <%s>: not a directory\n" % output_dir)
        sys.exit(1)

    input_filename = config.get('rstdiary', 'input')
    logging.debug("input_filename = %s" % input_filename)
    if not os.path.isfile(input_filename):
        sys.stderr.write("Invalid input: %s\n" % input_filename)
        sys.exit(1)

    parse_entries(input_filename)

    write_html()
    write_atom()


if __name__ == "__main__":
    main()
