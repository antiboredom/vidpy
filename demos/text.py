import random
from vidpy import Text, Clip, Composition

lines = '''A spectre is haunting Europe -
the spectre of communism.
All the powers of old Europe
have entered into a holy alliance
to exorcise this spectre:
Pope and Tsar,
Metternich and Guizot,
French Radicals and German police-spies.
Where is the party in opposition that
has not been decried as communistic by its opponents in power?
Where is the opposition
that has not hurled back
the branding reproach of communism,
against the more advanced opposition parties,
as well as against its reactionary adversaries?
Two things result from this fact:
I. Communism is already acknowledged
by all European powers to be itself a power.
II. It is high time that Communists should openly,
in the face of the whole world,
publish their views,
their aims,
their tendencies,
and meet this nursery tale
of the Spectre of Communism
with a manifesto of the party itself.'''.split('\n')

# some random style choices
fonts = ['Helvetica', 'Comic Sans MS', 'Andale Mono']
styles = ['normal', 'italic']
colors = ['#ff5179', '#43f8ff', '#a0ff5f', '#ffed00']

clips = []

for line in lines:
    # select random attributes
    font = random.choice(fonts)
    color = random.choice(colors)
    outline_color = random.choice(colors)
    outline_size = random.randint(3, 8)
    weight = random.randint(100, 1000)
    style = random.choice(styles)

    # put the text in a bounding box that fills 90% of the screen
    # (x, y, width, height)
    boundingbox = ('10%', '10%', '80%', '80%')

    # create a one second text clip with random parameters
    text = Text(line, end=1, color=color, font=font, style=style, weight=weight, olcolor=outline_color, outline=outline_size, size=200, bbox=boundingbox, pad=50)

    # add a glow for some reason!
    text.glow(1)

    clips.append(text)

comp = Composition(clips, singletrack=True, width=1280, height=720, fps=30)
comp.save('manifesto.mp4')
