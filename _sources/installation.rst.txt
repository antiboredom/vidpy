Installation
=================================

VidPy requires melt, which can be tricky to properly install on Mac and
Windows. The easiest option is to install Shotcut (an open source video
editor) which comes with a prebuilt melt binary.

Mac/Windows
-----------

1. `Download Shotcut <https://www.shotcut.org/download/>`_
2. Install it
3. Install VidPy with: ``pip install vidpy``

Ubuntu/Debian
-------------

1. Install melt: ``sudo apt-get install melt``
2. Install VidPy: ``pip install vidpy``

Setup
-----

VidPy will attempt to locate the melt binary, searching first for a
Shotcut installation on Mac/Windows. You can also point VidPy to a
specific binary like so:

.. code:: python

    import vidpy
    vidpy.MELT_BINARY = '/path/to/melt'
