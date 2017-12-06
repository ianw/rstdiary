# rstdiary

[![Build Status](https://travis-ci.org/ianw/rstdiary.svg?branch=master)](https://travis-ci.org/ianw/rstdiary)

Transform a flat rst text file into a simple HTML diary

## Input

The input is a single, flat RST file with one section per-day.  The
section must be titled with the date in `YYYY-MM-DD` form.  There is
also a special ``todo`` section that will be placed in a collapsed,
highlighted box on the first page.

Within each section, you can use most RST constructs to style text,
create lists or add links

An example input is

```rst
todo
====

* my
* todo
* list

2014-11-18
==========

*PTO*

2014-11-17
==========

Fixing bugs in old project

Started `a review <http://review.company.org/1234>`_ to fix broken
foobobnicator

2014-11-14
==========

Created git repos for new exciting project

* `<http://my-git.repo/project.git>`_
* `<http://my-git.repo/project-templates.git>`_
```

## Usage

`rstdiary` takes a single config-file as an argument

``` ini
[rstdiary]
input = example.rst
output_dir = /tmp
title = Worklog of Me
author_name = My Name
about = <a href="mailto:me@company.com">me@company.com</a>
site_root = http://foo.com/diary/
```

All of the above options should be filled out

## Output

`rstdiary` outputs one HTML page for each month of entries into
`output_dir`.  `index.html` is symlinked to the most recent month.

The output is lightly styled and uses CDN versions of some common
utilities such as bootstrap.

An atom feed of the entries for the latest month only is generated in
atom.xml

A sample output is [here](https://rawgit.com/ianw/rstdiary/master/sample/index.html)

## Installation

It is recommended to install via ``pip`` in a ``virtualenv``.  For a
working example, see [example](example/).