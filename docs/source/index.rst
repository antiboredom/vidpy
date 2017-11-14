.. meta::
   :description: Python video editor and compositor
   :title: VidPy
   :Author: Sam Lavigne
   :keywords: video, python


VidPy
=================================

A Python video editor and compositor based on the `MLT Multimedia
Framework <https://www.mltframework.org/>`_.

Note: VidPy is currently in alpha - there are probably a bunch of bugs, and
the api will likely change. If you’re interested in testing it out,
please do, and leave comments/suggestions/issues in the `issue
tracker <https://github.com/antiboredom/vidpy/issues>`_.

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/DzYvZx_eSRA" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>

.. code:: python

  from vidpy import Clip, Composition

  clips = []
  for i in range(0, 8):
      clip = Clip(vid, start=i*5)
      clip.repeat(5)
      clip.chroma(amount=.20)
      clip.position(x=i*160-500)
      clips.append(clip)

  comp = Composition(clips, bgcolor='#ff5179', duration=200)
  comp.save('hands.mp4')


.. toctree::
   :maxdepth: 4

   installation
   overview
   documentation
   examples


Credits
-------

VidPy is by `Sam Lavigne <http://lav.io>`__, and draws heavily from
`MoviePy by Zulko <http://zulko.github.io/moviepy/>`__.
