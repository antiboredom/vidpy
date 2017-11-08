VidPy
=====

.. image:: https://api.travis-ci.org/antiboredom/vidpy.svg
        :target: https://travis-ci.org/antiboredom/vidpy

A Python video editor and compositor based on the `MLT Multimedia
Framework <https://www.mltframework.org/>`__.

VidPy is currently in alpha - there are probably a bunch of bugs, and
the api will likely change. If you're interested in testing it out,
please do, and leave comments/suggestions/issues in the `issue
tracker <https://github.com/antiboredom/vidpy/issues>`__.

Read the full documentation here: https://antiboredom.github.io/vidpy

Installation/Dependencies
-------------------------

VidPy requires melt, which can be tricky to properly install on Mac and
Windows. The easiest option is to install Shotcut (an open source video
editor) which comes with a prebuilt melt binary.

Mac/Windows
~~~~~~~~~~~

1. `Install Shotcut <https://www.shotcut.org/download/>`__ (on a mac with brew: ``brew cask install shotcut``
2. Install VidPy with: ``pip install vidpy``

Ubuntu/Debian
~~~~~~~~~~~~~

1. Install melt: ``sudo apt-get install melt``
2. Install VidPy: ``pip install vidpy``

Setup
-----

VidPy will attempt to locate the melt binary, searching first for a
Shotcut installation on Mac/Windows. You can also point VidPy to a
specific binary like so:

.. code:: python

    from vidpy import config
    config.MELT_BINARY = '/path/to/melt'

Overview
--------

Use the ``Clip`` class to create and manipulate video clips, and the
``Composition`` class to put clips together.

``Composition()`` takes a list of clips as input, and then allows you to
save an output video with ``save()``, or to preview with ``preview()``.

By default a composition will treat each clip as a separate track,
playing them all at the same time.

.. code:: python

    from vidpy import Clip, Composition

    clip1 = Clip('video.mp4')
    clip2 = Clip('anothervideo.mp4')

    # play videos on top of each other
    composition = Composition([clip1, clip2])
    composition.save('output.mp4')

You can tell clips when to start playing with the ``offset`` parameter,
or with ``set_offset()`` after instantiation. All time is in seconds.

.. code:: python

    # start playing clip one after 1.5 seconds
    clip1 = Clip('video.mp4', offset=1.5)

    clip2 = Clip('anothervideo.mp4')
    clip2.set_offset(5) # start clip2 after 5 seconds

    composition = Composition([clip1, clip2])
    composition.save('output.mp4')

Trim clips with ``start`` and ``end`` parameters, or with the ``cut``
method.

.. code:: python

    # only use the first second of the clip
    clip1 = Clip('video.mp4', start=0, end=1)

    clip2 = Clip('anothervideo.mp4')
    clip2.cut(start=2, end=4) # use clip2 from 2 to 4 seconds

You can also play clips one after the other (instead of all at the same
time) by adding ``singletrack=True`` as a parameter to your composition.

.. code:: python

    composition = Composition([clip1, clip2], singletrack=True)
    composition.save('output.mp4')

``Composition`` also allows you to set dimensions, fps, and background
color.

.. code:: python

    # create a 1280x720 composition at 30 fps with a red background
    composition = Composition(clips, bgcolor="#ff0000", width=1280, height=720, fps=30)

    # preview it
    composition.preview()

Finally, you can convert compositions to clips to reuse.

.. code:: python

    comp = Composition([clip1, clip2, clip3], singletrack=True)
    clip = Clip(comp)

    # do stuff with the entire composition
    clip.cut(0, 1)

Filters & Effects
-----------------

There are a number of effects built into VidPy:

.. code:: python

    clip.fadein(1)      # fade the clip in over 1 second
    clip.fadeout(0.5)   # fade the clip over 0.5 seconds
    clip.glow()         # add a glow effect
    clip.spin(2)        # make the clip spin around. (Why would you do this? I don't know!)
    clip.chroma()       # attempt to automatically remove the background color
    clip.volume(0)      # mute a video

    # set clip's position 
    clip.position(x=100, y=20)

    # resize a clip
    clip.position(w='50%', h='20%'')

    # start the clip scaled to 200% at coordinates (0, 0)
    # then move it to (200, 200) and scale it to 90% over 5 seconds
    clip.zoompan([0, 0, '200%', '200%'], [200, 200, '90%', '90%'], start=0, end=5)

For a full list see the filters documentation: (link to come)

You can also use `any filter supported by
mlt <https://www.mltframework.org/plugins/PluginsFilters/>`__ with the
``fx`` method. The first parameter should be the name of the filter, and
the second a dictionary of options.

For example, to add a `cartoon
effect <https://www.mltframework.org/plugins/FilterFrei0r-cartoon/>`__:

.. code:: python

    # use the full filter name as the first parameter
    # and then a dictionary of options, based on the mlt documentation
    clip.fx('frei0r.cartoon', {'0': 0.999})

Or, `play with
colors <https://www.mltframework.org/plugins/FilterAvfilter-colorchannelmixer/>`__:

.. code:: python

    clip.fx('avfilter.colorchannelmixer', {'av.rr': 2, 'av.br': 2})

Remember to look at the mlt docs to figure out what parameters to pass
in.

Text
----

Use the ``Text`` class to add text clips

.. code:: python

    from vidpy import Text

    text_clip = Text("A spectre is haunting Europe.", font="Comic Sans Ms", size=100, color="#ff0000")

Some optional parameters for text clips are:

``font`` any font name on your system

``color`` color of text

``weight`` between 100 and 1000

``style`` normal or italic

``olcolor`` outline color

``outline`` outline size

``halign`` horizontal alignment (left, center, right)

``valign`` vertical alignment (top, middle, bottom)

``bbox`` a bounding box to put the text in (x, y, width, height)

Credits
-------

VidPy is by `Sam Lavigne <http://lav.io>`__, and draws heavily from
`MoviePy by Zulko <http://zulko.github.io/moviepy/>`__.
