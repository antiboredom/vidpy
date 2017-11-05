# VidPy

A Python video editor and compositor based on the [MLT Multimedia Framework](https://www.mltframework.org/).

* Installation
* Documentation
* Examples

## Installation/Dependencies

VidPy requires melt, which can be tricky to properly install on Mac and Windows. The easiest option is to install Shotcut (an open source video editor) which comes with a prebuilt melt binary.

### Mac/Windows

1. [Download Shotcut](https://www.shotcut.org/download/)
2. Install it
3. Install VidPy with: ```pip install vidpy```

### Ubuntu/Debian

1. Install melt: ```sudo apt-get install melt```
2. Install VidPy: ```pip install vidpy```

## Setup

VidPy will attempt to locate the melt binary, searching first for a Shotcut installation on Mac/Windows. You can also point VidPy to a specific binary like so:

```python
import vidpy
vidpy.MELT_BINARY = '/path/to/melt'
``` 

## Overview

Use the `Clip` class to create and manipulate video clips, and the `Composition` class to put clips together.

`Composition()` takes a list of clips as input, and then allows you to save an output video with `save()`, or to preview with `preview()`.

By default a composition will treat each clip as a separate track, playing them all at the same time.

```python
from vidpy import Clip, Composition

clip1 = Clip('video.mp4')
clip2 = Clip('anothervideo.mp4')

# play videos on top of each other
composition = Composition([clip1, clip2])
composition.save('output.mp4')
```

You can tell clips when to start playing with the `offset` parameter, or with `set_offset()` after instantiation. All time is in seconds.

```python
# start playing clip one after 1.5 seconds
clip1 = Clip('video.mp4', offset=1.5)

clip2 = Clip('anothervideo.mp4')
clip2.set_offset(5) # start clip2 after 5 seconds

composition = Composition([clip1, clip2])
composition.save('output.mp4')
```

Trim clips with `start` and `end` parameters, or with the `cut` method.

```python
# only use the first second of the clip
clip1 = Clip('video.mp4', start=0, end=1)

clip2 = Clip('anothervideo.mp4')
clip2.cut(start=2, end=4) # use clip2 from 2 to 4 seconds
```

You can also play clips sequentially by adding `singletrack=True` as a parameter.

```python
composition = Composition([clip1, clip2], singletrack=True)
composition.save('output.mp4')
```

`Composition` also allows you to set dimensions, fps, and background color.

```python
# create a 1280x720 composition at 30 fps with a red background
composition = Composition(clips, bgcolor="#ff0000", width=1280, height=720, fps=30)

# preview it
composition.preview()
```

Finally, you can convert compositions to clips to reuse.

```python
comp = Composition([clip1, clip2, clip3], singletrack=True)
clip = Clip(comp)

# do stuff with the entire composition
clip.cut(0, 1)
```

## Filters & Effects

You can assign filters to clips.

```python
clip.fadein(1) 		# fade the clip in over 1 second
clip.fadeout(0.5) 	# fade the clip over 0.5 seconds
clip.glow()   		# add a glow effect
clip.spin(2)  		# make the clip spin around
clip.chroma() 		# attempt to automatically remove the background color
```

For a full list see the filters documentation: (link to come)

You can also add [any filter supported by mlt](https://www.mltframework.org/plugins/PluginsFilters/) with the `fx` method.

For example, to add a [cartoon effect](https://www.mltframework.org/plugins/FilterFrei0r-cartoon/):



```python
# use the full filter name as the first parameter
# and then a dictionary of options, based on the mlt documentation
clip.fx('frei0r.cartoon', {'0': 0.999})
```

Or, [play with colors](https://www.mltframework.org/plugins/FilterAvfilter-colorchannelmixer/):

```python
clip.fx('avfilter.colorchannelmixer', {'av.rr': 2, 'av.br': 2})
```

Remember to look at the mlt docs to figure out what parameters to pass in.

## Text

Use the `Text` class to add text clips

```python
from vidpy import Text

text_clip = Text("A spectre is haunting Europe.", font="Comic Sans Ms", size=100, color="#ff0000")
```

Some optional parameters for text clips are:

`font` any font name on your system

`color` color of text

`weight` between 100 and 1000

`style` normal or italic

`olcolor` outline color

`outline` outline size

`halign` horizontal alignment (left, center, right)

`valign` vertical alignment (top, middle, bottom)

`bbox` a bounding box to put the text in (x, y, width, height)

## Credits

VidPy is by Sam Lavigne, and heavily inspired by / indebted to MoviePy by Zulko.



