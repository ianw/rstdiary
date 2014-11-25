# rstdiary

Transform a flat rst text file into a simple HTML diary

## input

The input is a single, flat RST file with one section per-day.  The section must be titled with the date in `YYYY-MM-DD` form.  No other sections should be used in the file.

Within each section, you can use most RST constructs to style text, create lists or add links

An example input is

```rst
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

## usage

`rstdiary` takes a single config-file as an argument

``` ini
[rstdiary]
input = example.rst
output_dir = /tmp
title = Worklog of Me
about = <a href="mailto:me@company.com">me@company.com</a>
```

All of the above options should be filled out

## output

`rstdiary` outputs one HTML page for each month of entries into
`output_dir`.  `index.html` is symlinked to the most recent month.

The output is lightly styled and uses CDN versions of some common
utilities such as bootstrap.

A sample output is [here](https://rawgit.com/ianw/rstdiary/master/sample/index.html)