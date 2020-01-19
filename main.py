from psychopy import prefs
prefs.hardware['audioLib'] = ['pyo']
# prefs.hardware['audioLatencyMode'] = '3'  # Aggressive exclusive mode in PTB
from psychopy import visual, event, core, monitors, microphone, gui, sound
import psychopy.tools.coordinatetools
import random
import numpy as np
import csv
import os
from guimy import present_gui

# Enable sound input/output: you need to do this well before you actually record anything, it is like 'power on'
microphone.switchOn(sampleRate=16000)

dlg = present_gui()
participant = dlg['Participant ID']
age = dlg["Participant Age"]
sex = dlg["Participant Sex"]
condition = dlg["Condition"]

print("")
print(condition)
print("")

which_stimulus_size = dlg["Stimulus size"]

# initialise the monitor
mon = monitors.Monitor("e330", width=30.0, distance=60.0)
mon.saveMon()
mon.setSizePix((1920, 1080))

# open the window
if which_stimulus_size == "window":
    win = visual.Window(fullscr=False,  size=[900, 900], screen=0, color=[0, 0, 0], units="pix", allowGUI=True,
                        waitBlanking=True, monitor=mon, autoLog=False, winType='pyglet', gammaErrorPolicy="ignore")
elif which_stimulus_size == "fullscreen":
    win = visual.Window(fullscr=True, size=[1920, 1080], units='pix', winType='pyglet', monitor=mon)

# specify the coordinates of the numbers on the clock perimeter
thetas = np.linspace(start=360+90, stop=90, num=12, endpoint=False, retstep=False, dtype='f8')
xs, ys = psychopy.tools.coordinatetools.pol2cart(thetas, radius=300+30)
text_positions = list(zip(xs, ys))

# give the coordinates of each increment's position on the clock perimeter, for use in rotating the hand smoothly
thetas = np.linspace(start=360+90, stop=90, num=60*4, endpoint=False, retstep=False, dtype='f8')
xs, ys = psychopy.tools.coordinatetools.pol2cart(thetas, radius=300)
second_positions = list(zip(xs, ys))

# Make a stimulus for the clock's perimeter
clock_circle = visual.Circle(win, radius=300, edges=32*8, pos=(0, 0), name='clock')

# Make a not-shown circle with 12 edges for tick mark positions
tick_circle_start_major = visual.Circle(win, radius=300, edges=12, pos=(0, 0))
tick_circle_end_major =   visual.Circle(win, radius=300+13, edges=12, pos=(0, 0))
tick_circle_start_minor = visual.Circle(win, radius=300, edges=60, pos=(0, 0))
tick_circle_end_minor =   visual.Circle(win, radius=300+7, edges=60, pos=(0, 0))

# Make a stimulus for the clock's centre
clock_centre = visual.Circle(win, radius=5, edges=32*8, pos=(0, 0), name='center', fillColor='white')

# specify the text for the numbers on the clock face
clock_text = ['60'] + [str(x) for x in range(5, 60, 5)]

# draw the clock into a movie frame
for i in range(12):
    txt = visual.TextStim(win=win, text=clock_text[i], pos=text_positions[i], alignHoriz='center', alignVert='center')
    txt.draw()
    maj = visual.Line(win, start=tick_circle_start_major.vertices[i], end=tick_circle_end_major.vertices[i])
    maj.draw()
for j in range(60):
    minor = visual.Line(win, start=tick_circle_start_minor.vertices[j], end=tick_circle_end_minor.vertices[j])
    minor.draw()
clock_circle.draw()
clock_centre.draw()
win.getMovieFrame(buffer='back')
win.saveMovieFrames("clock.jpg")
win.clearBuffer()

clock_stimulus = visual.ImageStim(win, image="clock.jpg")

trials = [1, 2]
max_trial = trials[len(trials)-1]

# Start the session
session = {}
# Trial loop
for trial_number in trials:
    trial_name = str(trial_number)
    wave_file_name = str(participant) + "_trial_" + str(trial_number)
    key__real_time_on = 0.0
    key__face_time_on = 0.0
    session[trial_number] = {
        "participant": participant,
        "age": age,
        "sex": sex,
        "trial_number": trial_number,
        "trial_name": trial_name,
        "trial_condition": condition,
        "wave_file_name": wave_file_name,
        "key__real_time_on": 0.0,
        "tone_real_time_on": 0.0,
        "key__face_time_on": 0.0,
        "tone_face_time_on": 0.0,
    }
    results_file_name = os.path.join("results", "participant_{}.csv".format(participant))
    trial_clock = None
    started = False
    start_key = []
    timer_on = False
    response_key_pressed = False
    clock_time_in_seconds = None
    countdown = None
    post_keypress_rotation_duration = random.randrange(start=1500, stop=2500, step=1) / 1000.0
    keys = []
    tone_played = False
    fake_keypress_time = random.randrange(start=1000, stop=5000, step=1) / 1000
    wave_file_directory = 'wave_files'
    wave_file_duration = 5
    request_estimate_text = None
    if condition in ['action-effect tone', 'baseline tone']:
        request_estimate_text = "When did you hear the tone?"
    if condition in ['action-effect action', 'baseline action']:
        request_estimate_text = "When did you press the key?"
    print('waiting for keypress')
    while not started:
        event.clearEvents()
        if not started and not timer_on:
            start_instructions = visual.TextStim(win, text="Press any key to start the clock")
            start_instructions.draw()
            win.flip()
            start_key = event.getKeys()
            if len(start_key) and start_key[0] == 'escape':
                print('user quitted')
                core.quit()
            started = True if len(start_key) else False
            event.clearEvents()
        if started and not timer_on:
            timer_on = True
            trial_clock = core.Clock()
        if started and timer_on:
            for number_of_revolutions in range(2):
                for secs in range(60*4):
                    clock_stimulus.draw()
                    hand = visual.Line(win, start=(0, 0), end=second_positions[secs], lineWidth=8)
                    hand.draw()
                    if not response_key_pressed:
                        keys = event.getKeys(timeStamped=trial_clock)
                    if not response_key_pressed and len(keys):
                        response_key_pressed = True
                        event.clearEvents()
                        key__real_time_on = float(keys[0][1])
                        key__face_time_on = float(secs / 4.0)
                        session[trial_number]["key__real_time_on"] = round(key__real_time_on, 4)
                        session[trial_number]["key__face_time_on"] = key__face_time_on
                        countdown = core.CountdownTimer(start=post_keypress_rotation_duration)
                    if response_key_pressed and condition in ['action-effect tone', 'action-effect action'] and not tone_played:
                        if trial_clock.getTime() - key__real_time_on >= 0.250:
                            tone_real_time_on = trial_clock.getTime()
                            tone_face_time_on = (secs / 4.0)
                            session[trial_number]["tone_real_time_on"] = round(tone_real_time_on, 4)
                            session[trial_number]["tone_face_time_on"] = round(tone_face_time_on, 4)
                            tone = sound.Sound(value=1000, secs=0.075)
                            tone.play()
                            tone_played = True
                    if not response_key_pressed and condition in ['baseline tone'] and not tone_played:
                        if trial_clock.getTime() >= fake_keypress_time:
                            tone_real_time_on = trial_clock.getTime()
                            tone_face_time_on = (secs / 4.0)
                            session[trial_number]["tone_real_time_on"] = round(tone_real_time_on, 4)
                            session[trial_number]["tone_face_time_on"] = round(tone_face_time_on, 4)
                            tone = sound.Sound(value=1000, secs=0.075)
                            tone.play()
                            tone_played = True
                    if response_key_pressed and condition in ['baseline action']:
                        pass
                    if response_key_pressed and countdown.getTime() <= 0:
                        win.flip()
                        break
                    win.flip()

    trial_microphone = microphone.AudioCapture(name=wave_file_name, saveDir=wave_file_directory, stereo=False, chnl=0)
    trial_microphone.reset()
    request = visual.TextStim(win, request_estimate_text)
    request.draw()
    win.flip()
    trial_microphone.record(sec=wave_file_duration, block=False)
    trial_microphone.reset()
    core.wait(wave_file_duration)
    win.flip()

    if trial_number < max_trial:
        iti = visual.TextStim(win, "Get ready for the next trial ...")
        iti.draw()
    win.flip()
    core.wait(2)

    print("")
    for k, v in session[trial_number].items():
        print("{}\t{}".format(k, v))
    print("")

w = csv.writer(open(results_file_name, "w"))
for t in trials:
    this_trial = session[t]
    for key, val in this_trial.items():
        w.writerow([key, val])
