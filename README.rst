scons-tool-gnuplot
==================

.. image:: https://badge.fury.io/py/scons-tool-gnuplot.svg
    :target: https://badge.fury.io/py/scons-tool-gnuplot
    :alt: PyPi package version

.. image:: https://travis-ci.org/ptomulik/scons-tool-gnuplot.svg?branch=master
    :target: https://travis-ci.org/ptomulik/scons-tool-gnuplot
    :alt: Travis CI build status

.. image:: https://ci.appveyor.com/api/projects/status/github/ptomulik/scons-tool-gnuplot?svg=true
    :target: https://ci.appveyor.com/project/ptomulik/scons-tool-gnuplot

Gnuplot tool for scons_. For tarball and documentation see `project page at
sourceforge.net`_.

INSTALLATION
------------

There are few ways to install this tool for your project.

From pypi_
^^^^^^^^^^

This method may be preferable if you build your project under a virtualenv. To
add gnuplot tool from pypi_, type (within your wirtualenv):

.. code-block:: shell

   pip install scons-tool-loader scons-tool-gnuplot

or, if your project uses pipenv_:

.. code-block:: shell

   pipenv install --dev scons-tool-loader scons-tool-gnuplot

Alternatively, you may add this to your ``Pipfile``

.. code-block::

   [dev-packages]
   scons-tool-loader = "*"
   scons-tool-gnuplot = "*"


The tool will be installed as a namespaced package ``sconstool.gnuplot``
in project's virtual environment. You may further use scons-tool-loader_
to load the tool.

As a git submodule
^^^^^^^^^^^^^^^^^^

#. Create new git repository:

   .. code-block:: shell

      mkdir /tmp/prj && cd /tmp/prj
      touch README.rst
      git init

#. Add the `scons-tool-gnuplot`_ as a submodule:

   .. code-block:: shell

      git submodule add git://github.com/ptomulik/scons-tool-gnuplot.git site_scons/site_tools/gnuplot

#. For python 2.x create ``__init__.py`` in ``site_tools`` directory:

   .. code-block:: shell

      touch site_scons/site_tools/__init__.py

   this will allow to directly import ``site_tools.gnuplot`` (this may be required by other tools).


REQUIREMENTS
------------

To perform certain activities, you may need the following packages (listed per
task).

To generate API documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- epydoc_,
- python-docutils_,
- python-pygments_.

To generate user documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- docbook-xml_,
- xsltproc_,


GENERATING DOCUMENTATION
------------------------

Scons gnuplot tool has an API documentation and user manual. The documentation
may be generated as follows (see also REQUIREMENTS).

API documentation
^^^^^^^^^^^^^^^^^

Before generating API docs, you should install our module in edit mode::

   pipenv run pip install -e .

To generate API documentation type::

   pipenv run scons api-doc

The generated API documentation will be written to ``build/doc/api/``. Note,
that API doc generator (epydoc) works only with python2.

User manual
^^^^^^^^^^^

To generate user manual type::

   pipenv run scons user-doc

The generated documentation will be written to ``build/doc/user/``.

LICENSE
-------
Copyright (c) 2013-2020 by Paweł Tomulik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE

.. _curl: http://curl.haxx.se/
.. _scons: https://bitbucket.org/scons/scons
.. _epydoc: http://epydoc.sourceforge.net/
.. _python-docutils: http://pypi.python.org/pypi/docutils
.. _python-pygments: http://pygments.org/
.. _docbook-xml: http://www.oasis-open.org/docbook/xml/
.. _xsltproc: http://xmlsoft.org/libxslt/
.. _scons docbook tool: https://bitbucket.org/dirkbaechle/scons_docbook/
.. _project page at sourceforge.net: http://sourceforge.net/projects/scons-gnuplot/
.. _pipenv: https://pipenv.readthedocs.io/
.. _pypi: https://pypi.org/
.. _scons-tool-loader: https://github.com/ptomulik/scons-tool-loader/

.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->
