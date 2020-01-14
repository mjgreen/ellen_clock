import numpy as np
from psychopy import visual, event, core, monitors
import psychopy.tools.coordinatetools

# initialise the monitor
mon = monitors.Monitor("e330", width=30.0, distance=60.0)
mon.saveMon()
mon.setSizePix((1920, 1080))

# open the window
win = visual.Window(fullscr=False,  size=[900, 900], screen=0, color=[0, 0, 0], units="pix", allowGUI=True,
                    waitBlanking=True, monitor="e330", autoLog=False, winType='pyglet', gammaErrorPolicy="ignore")

# specify the coordinates of the numbers on the clock perimeter
thetas = np.linspace(start=360+90, stop=90, num=12, endpoint=False, retstep=False, dtype='f8')
xs, ys = psychopy.tools.coordinatetools.pol2cart(thetas, radius=300+20)
xs = xs + 1920/4.0
coords = list(zip(xs, ys))

# give the coordinates of each increment's position on the clock perimeter, for use in rotating the hand smoothly
thetas = np.linspace(start=360+90, stop=90, num=60*4, endpoint=False, retstep=False, dtype='f8')
xs, ys = psychopy.tools.coordinatetools.pol2cart(thetas, radius=300)
second_positions = list(zip(xs, ys))

# Make a stimulus for the clock's perimeter
clock_circle = visual.Circle(win, radius=300, edges=32*8, pos=(0, 0), name='clock')

# Make a stimulus for the clock's centre
clock_centre = visual.Circle(win, radius=5, edges=32*8, pos=(0, 0), name='center', fillColor='white')

# specify the text for the numbers on the clock face
clock_text = ['60'] + [str(x) for x in range(5, 60, 5)]

# draw the clock into a movie frame
# TODO add tick marks
clock_circle.draw()
clock_centre.draw()
for i in range(12):
    txt = visual.TextStim(win=win, text=clock_text[i], pos=coords[i])
    txt.draw()
win.getMovieFrame(buffer='back')
win.saveMovieFrames("clock.jpg")

clock_stimulus = visual.ImageStim(win, image="clock.jpg")


# Draw the clock, and make the hand sweep round a few times

for number_of_revolutions in range(2):
    for secs in range(60*4):
        myline = visual.Line(win, start=(0, 0), end=second_positions[secs], lineWidth=8)
        clock_stimulus.draw()
        myline.draw()
        win.flip()



# event.waitKeys()