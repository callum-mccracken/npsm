===================
2. raising_lowering
===================

Once you've run ncsd, you have eigenvectors of nuclei in one particular
angular momentum state. For the next few calculations, you're going to need
more angular momentum states.

So we could run ncsd again and again, but that would take forever, so instead
we apply `the raising/lowering opperators for J <https://en.wikipedia.org/wiki/Ladder_operator>`_
to our state.

There's just one module here, open it, adjust a few parameters, and run it::

    python shift_j.py

shift_j.py
==========

.. automodule:: raising_lowering.shift_j
   :members:
