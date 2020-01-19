import numpy as np
from psychopy import visual, event, core, monitors
import psychopy.tools.coordinatetools
import random
# from mygui import present_gui

# dlg = present_gui()
# condition = dlg['Condition']
condition = 'baseline action'
condition = 'action-effect: tone'
print(condition)
which_window_size = "fullscreen"
which_window_size = "small"

# initialise the monitor
mon = monitors.Monitor("e330", width=30.0, distance=60.0)
mon.saveMon()
mon.setSizePix((1920, 1080))

# open the window
if which_window_size == "small":
    win = visual.Window(fullscr=False,  size=[900, 900], screen=0, color=[0, 0, 0], units="pix", allowGUI=True,
                        waitBlanking=True, monitor=mon, autoLog=False, winType='pyglet', gammaErrorPolicy="ignore")
elif which_window_size == "fullscreen":
    win = visual.Window(fullscr=True, size=[1920, 1080], units='pix', winType='pyglet', monitor=mon)

# specify the coordinates of the numbers on the clock perimeter
thetas = np.linspace(start=360+90, stop=90, num=12, endpoint=False, retstep=False, dtype='f8')
xs, ys = psychopy.tools.coordinatetools.pol2cart(thetas, radius=300+20)
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
for i in range(12):
    txt = visual.TextStim(win=win, text=clock_text[i], pos=coords[i])
    txt.draw()
clock_circle.draw()
clock_centre.draw()
win.getMovieFrame(buffer='back')
win.saveMovieFrames("clock.jpg")
win.clearBuffer()

clock_stimulus = visual.ImageStim(win, image="clock.jpg")


# Draw the clock, and make the hand sweep round a few times
started = False
timer_on = False
response_key_pressed = False
clock_time_in_seconds = None
countdown = None
post_keypress_rotation_duration = 0.0
keys = []
foo = 0
print('waiting for keypress')
while not started:
    event.clearEvents()
    if not started and not timer_on:
        start_instructions = visual.TextStim(win, text="Press any key to start the clock")
        start_instructions.draw()
        win.flip()
        started = True if len(event.getKeys()) else False
        event.clearEvents()
    if started and not timer_on:
        timer_on = True
        experiment_clock = core.Clock()
        t0 = experiment_clock.getTime()
        print("t0 = {}".format(round(t0)))
    if started and timer_on:
        for number_of_revolutions in range(2):
            for secs in range(60*4):
                clock_stimulus.draw()
                hand = visual.Line(win, start=(0, 0), end=second_positions[secs], lineWidth=8)
                hand.draw()
                true_clockface_time_elapsed = (number_of_revolutions * 60) + (secs / 4.0)
                true_clockface_time = secs / 4.0
                if secs % 4 == 0:
                    clock_time_in_seconds = visual.TextStim(win, text=str(true_clockface_time), pos=(400, 400))
                clock_time_in_seconds.draw()
                if not response_key_pressed:
                    keys = event.getKeys(timeStamped=experiment_clock)
                if not response_key_pressed and len(keys):
                    key_time = keys[0][1]
                    print("key_time = {} seconds on the experiment clock python object".format(key_time))
                    print("true_clockface_time = {} seconds on the clock face".format(true_clockface_time))
                    print("true_clockface_time_elapsed = {} seconds of clockface time".format(true_clockface_time_elapsed))
                    response_key_pressed = True
                    event.clearEvents()
                    post_keypress_rotation_duration = random.randrange(start=1500, stop=2500, step=1) / 1000.0
                    print("post_keypress_rotation_duration = {} seconds".format(post_keypress_rotation_duration))
                    countdown = core.CountdownTimer(start=post_keypress_rotation_duration)

                if response_key_pressed and countdown.getTime() <= 0:
                    break

                if response_key_pressed and condition in ['action-effect: action', 'action-effect: tone']:
                    if experiment_clock.getTime() - key_time >= 0.250:
                        if foo == 0:
                            print('250 ms have elapsed since key_time')
                            foo = 1
                        # play_a_tone()
                        pass

                win.flip()

