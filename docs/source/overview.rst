Overview
========

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
