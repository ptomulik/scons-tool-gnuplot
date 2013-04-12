scons-tool-gnuplot
==================

Gnuplot tool for scons_.

INSTALLATION
------------

Copy the ``gnuplot/`` directory to your project's ``site_scons/site_tools/`` or
to ``~/.scons/site_scons/site_tools/`` (per user configuration). See SCons manual
for details.


REQUIREMENTS
------------

TO DOWNLOAD DEPENDENCIES FROM EXTERNAL REPOSITORIES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  - mercurial_ VCS (``hg``) 

TO RUN TESTS
^^^^^^^^^^^^

  - scons_test_framework_ by Dirk Baechle, 

TO GENERATE API DOCUMENTATION
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  - epydoc_,
  - python-docutils_,
  - python-pygments_.

TO GENERATE USER DOCUMENTATION
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  - docbook-xml_,
  - xsltproc_,

and (locally downloaded)

  - `scons docbook tool`_.

ADDITIONAL STEPS
----------------

If this is a fresh clone/checkout from repository, you may wish to perform a
few additional steps as below

DOWNLOAD DEPENDENCIES FROM EXTERNAL REPOSITORIES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some files from external projects need to be downloaded into the
development tree (they are usually not a part of any installable package). The
files are obtainable from external repositories, and may be easily downloaded
on GNU systems with the script ``bin/download-deps.sh`` ::

    bin/download-deps.sh

Particular projects, that this project depends on, are mentioned in the
following subsections.

TESTING FRAMEWORK
^^^^^^^^^^^^^^^^^

If you wish to run end-to-end tests for this tool, download the testing
framework for scons extensions/tools (currently from Dirk Baechle's repository
scons_test_framework_ hosted on bitbucket.org). The following files/directories
need to be downloaded (and placed as shown in table relative to the top-level
source directory)

 ========================= ==================================================
  source file/directory                   target file/directory
 ========================= ==================================================
  ``QMTest/``               ``QMTest/``
 ------------------------- --------------------------------------------------
  ``runtest.py``            ``runtest.py``
 ========================= ==================================================

On GNU system you may use the ``bin/download-test-framework.sh``  script to
download the testing framework (requires ``hg`` to be installed on your system)::

    bin/download-test-framework.sh

This script downloads and copies to the top-level directory the ``QMTest``
package and ``runtest.py`` script from the repository. The test framework may
be later removed with the ``bin/delete-test-framework.sh`` script::

    bin/delete-test-framework.sh

You may also delete manually files/directories comprising the framework.

The testing framework is ignored by ``.gitignore``, so you don't have to worry
about deleting it before doing commits.

SCONS DOCBOOK TOOL
^^^^^^^^^^^^^^^^^^

If you wish to generate user's guide, you need to download locally the `scons
docbook tool`_. It is obtainable from Dirk Baechle's repository hosted on
bitbucket.org. The following files/directories need to be downloaded (and
placed as shown in table relative to the top-level source directory)

 ========================= =====================================================
  source file/directory                   target file/directory
 ========================= =====================================================
  ``__init__.py``           ``site_scons/site_tools/docbook/__init__.py``
 ------------------------- -----------------------------------------------------
  ``utils/``                ``site_scons/site_tools/docbook/utils``
 ------------------------- -----------------------------------------------------
  ``docbook-xsl-<ver>/``    ``site_scons/site_tools/docbook/docbook-xsl-<ver>``
 ========================= =====================================================

RUNNING TESTS
-------------

To run all the tests type::
  
    python runtest.py -a

This requires the presence of the testing framework in the development tree.

GENERATING DOCUMENTATION
------------------------

API DOCUMENTATION
^^^^^^^^^^^^^^^^^

To generate API documentation type::

    scons api-doc

The generated API documentation will be written to ``build/doc/api/``.

USER MANUAL
^^^^^^^^^^^

To generate user manual type::

    scons user-doc

The generated documentation will be written to ``build/doc/user/``.

LICENSE
-------
Copyright (c) 2013 by Pawel Tomulik

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

.. _scons: http://scons.org
.. _scons_test_framework: https://bitbucket.org/dirkbaechle/scons_test_framework
.. _mercurial: http://mercurial.selenic.com/
.. _epydoc: http://epydoc.sourceforge.net/
.. _python-docutils: http://pypi.python.org/pypi/docutils
.. _python-pygments: http://pygments.org/
.. _docbook-xml: http://www.oasis-open.org/docbook/xml/
.. _xsltproc: http://xmlsoft.org/libxslt/
.. _scons docbook tool: https://bitbucket.org/dirkbaechle/scons_docbook/
