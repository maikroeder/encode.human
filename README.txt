.. contents::

Introduction
============

The ENCODE RNA Dashboard (hg19) provides a summary of transcriptome data production within the ENCODE project.

    http://genome.crg.es/encode_RNA_dashboard/hg19/

You can either reproduce this dashboard, or change the way it is rendered, by reconfiguring it.

Installation
============

In order to install the dependencies, run:

    make build

This will install the right Python packages and put the necessary scripts into the bin folder.

Dashboard Generation
====================

The ENCODE Human dashboard data is read from the following location:

    encode/human/apache_export/hg19_RNA_dashboard_files.txt

The following command renders the ENCODE Human dashboard with Pigeonhole:

    ./bin/pigeonhole dashboard.txt -v -c encode/human/page/page.ini -O encode/human/apache_export encode/human/page/input

You can then open the resulting dashboard:

    encode/human/apache_export/index.html

Reconfiguration
===============

You can easily reconfigure the dashboard by changing some of the dimensions.

For example if you want to show the RNA Fraction at the place of the Compartment, you could change the following file

    encode/human/level_1.ini

and reconfigure the right_row, column and dimensions settings:

    right_row: compartment
    column: rnaextract
    dimensions: cell strain age sex compartment rnaextract technology

When you render the dashboard again, you will see the RNA Fractions used for the columns, and the compartment in the right row.

Implementation
==============

Pigeonhole extends mr.bob, a flexible tool specially designed for rendering directory structure templates. The documentation for mr.bob is available here:

    https://github.com/iElectric/mr.bob.git

The development of the individual templates that are used for rendering a complete dashboard is refreshingly simple with mr.bob, as you will see in the next section. Right now we will have a look at how Pigeonhole is implemented by internally calling mr.bob.

In an initial phase, Pigeonhole reads the dashboard.txt file that contains the exact command line calls for rendering the templates with mr.bob, and runs all of them internally for reusing them in the next phase.

The command line contains a number of options after "dashboard.txt" that are reproduced here:

    -v -c encode/human/page/page.ini -O encode/human/apache_export encode/human/page/input

Pigeonhole internally calls mr.bob with these parameters, only this time the the top level template contained in 

    encode/human/page

renders lower level templates recursively through callback slots embedded in the templates, that were ignored in the initial phase. Here is an example of a simple slot that embeds the header template inside the page template:

    <tal:block content="structure python:slot('header')" />

Some callbacks pass on a reduced data set of the ENCODE Human dashboard, for example the tables template that repeatedly calls the subtable template with a different group of data:

    <div tal:content="structure python:slot('subtable', grouped.get_group(cell_key))">

The data set is reduced until the lowest level has been reached, and templates are inserted recursively into upper level templates.


Template Preview
================

The templates that make up the dashboard can be rendered in batch mode:

    source dashboard.txt

You can now preview all the rendered templates:

    open encode/human/*/output/*.html

If you want to experiment with the mr.bob parameters, you can also render them individually like this:

    ./bin/mrbob -v -c encode/human/header/header.ini -O encode/human/header/output encode/human/header/input

In this example, the result can be previewed in a browser by opening

    open encode/human/header/output/header.html

The templates here use the whole data from the ENCODE Human dashboard, which makes them bulky, but it does have two great advantages:

1. It is rather practical to get a good overview of how the rendering will look for all the different types of data. 

2. Rendering all data will also make sure that the template will not break later when rendering the whole dashboard, while reporting no problems with a limited data set.

Dependencies
============

The ENCODE RNA Dashboard (mm9) is produced with the help of the following Open Source Python packages:

- For rendering, the zope.pagetemplate module is used:
  https://pypi.python.org/pypi/zope.pagetemplate

- Pandas provides the data structures:
  https://pypi.python.org/pypi/pandas

- mr.bob is used to render the templates individually:
  https://pypi.python.org/pypi/mr.bob

- Pigeonhole is used for assembling the dashboard from the templates:
  https://pypi.python.org/pypi/pigeonhole
