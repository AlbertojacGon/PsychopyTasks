from psychopy import core, visual, event
import random

FULL_SCREEN=False
N_TRIALS = 100
STIM_TIME = 0.7
ISI = 1

win = visual.Window(size=(800, 768), fullscr=FULL_SCREEN, color='black')

words = [ "red", "green", "blue"]
colors = ["red","green","blue"]

stim = visual.TextStim(win=win, text= '',height=0.3, wrapWidth=1.5, color="white")

globalClock = core.Clock()
trialClock = core.Clock()
rts = []
trialTypes = []
responses = []
shownWords = []
shownColors = []
for trial in range(N_TRIALS):
    responded = False
    trialType = random.choice(["congruent","incongruent"])
    trialTypes.append(trialType)
    if trialType == 'congruent':
        word = random.choice(words)
        color = word
    else:
        word = random.choice(words)
        available_colors = colors[:]
        available_colors.remove(word)
        color = random.choice(available_colors)

    stim.setText(word)
    stim.setColor(color)
    shownWords.append(word)
    shownColors.append(color)
    event.clearEvents()
    stim.draw()
    win.flip()
    trialClock.reset()
    while trialClock.getTime() < STIM_TIME:
        core.wait(0.002)
        response = event.getKeys(keyList= ['1','2','3'])
        if response and not responded:
            rt = trialClock.getTime()
            rts.append(rt)
            responses.append(response[0])
            responded = True
    win.flip()
    while trialClock.getTime() < STIM_TIME + ISI:
        core.wait(0.002)
        response = event.getKeys(keyList= ['1','2','3','escape'])
        if response:
            if response[0] == 'escape':
                win.close()
                core.quit()
        if response and not responded:
            rt = trialClock.getTime()
            rts.append(rt)
            responses.append(response[0])
            responded = True
    if not responded:
        rts.append('_')
        responses.append('_')
win.close()

from datetime import datetime
dt = "{:%d_%B_%Y_%Hh%Mm}".format(datetime.now())

import csv
with open('session' + dt + '.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(rts)
    wr.writerow(trialTypes)
    wr.writerow(responses)
    wr.writerow(shownWords)
    wr.writerow(shownColors)
