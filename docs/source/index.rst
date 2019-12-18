======================
No Pain Shell Model
======================

.. mdinclude:: ../../README.md

Links
-----------

.. toctree::
   :maxdepth: 1

   table_of_contents/walkthrough/walkthrough
   table_of_contents/ncsd_python/ncsd_python
   table_of_contents/raising_lowering/raising_lowering
   table_of_contents/trdens_python/trdens_python
   table_of_contents/ncsmc_python/ncsmc_python
   table_of_contents/cross_sections/cross_sections

To Edit these Docs
------------------

These docs were created by sphinx, which pulls docstrings from Python modules.
It's not fully automatic though, so if you add a new file to the file structure,
don't expect it to be added to the docs!
This was intentional since it forced me to actually look at the docs
and make sure they looked decent, but if you want to make it more automatic,
go ahead!

To generate new HTML files:

1. You will need to install a few packages, ``m2r`` and ``sphinx_rtd_theme``.
2. Then, ``cd`` into ``docs`` then run a sphinx command like ``make html``.

To add a new Python module:

1. Create the Python file, and make sure it has well-formatted reST docstrings. `Documentation is here <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_.
2. Create ``docs/source/your_filename.rst``, just copy & edit one that's there.
3. Edit ``docs/source/index.rst`` so it includes your new file.
4. Then generate new HTML files, see above.

To look at the docs locally without pushing to GitHub:

1. ``python -m http.server 1234``.
2. Go to this url: ``http://localhost:1234/docs/build/html/``.
3. You may have to force a hard reset to see your changes,
   ``cmd + shift + R`` on Chrome for OSX.
