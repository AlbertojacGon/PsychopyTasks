#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MID Task
"""


from __future__ import division
from psychopy import core, data, event, visual, gui
import os, sys
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


# Some paramenters
FULL_SCREEN = True

targetDurationI = 0.3 # initial target duration
cueDuration = 1.5 #0.6
fbDuration = 1
TfbDuration = 1#.8
ISI1dur = 0.5 # sera NULL
ISI2dur = 2 # Cue-Target
ISI3dur = 1 # target-Fb
ISI4dur = 0.0 #0.5
Money = 2.5


seq1 = ["N", "L", "L", "N", "N", "L", "W", "L", "W", "L", "L", "L", "L", "W", \
        "L", "L", "N", "L", "N", "L", "L", "L", "W", "L", "L", "W", "W", "W", \
        "L", "W", "L", "L", "N", "W", "W", "W", "W", "W", "N", "W", "W", "L", \
        "W", "N", "N", "W", "W", "L", "W", "N", "N", "W", "W", "L", "W", "W", \
        "W", "N", "L", "L"]
seq2 = ["W", "L", "W", "L", "W", "L", "N", "N", "W", "W", "L", "L", "N", "W",\
        "W", "N", "L", "W", "L", "L", "W", "W", "W", "L", "L", "N", "N", "L", \
        "W", "N", "L", "N", "W", "L", "W", "L", "L", "W", "W", "L", "L", "L", \
        "W", "W", "L", "N", "L", "L", "L", "L", "N", "W", "W", "L", "N", "W", \
        "N", "W", "W", "W"]
seq3 = ["W", "L", "L", "W", "L", "N", "N", "L", "W", "W", "W", "L", "W", "L",\
        "N", "N", "W", "L", "L", "L", "L", "N", "W", "L", "W", "W", "L", "L", \
        "W", "W", "L", "W", "W", "N", "W", "L", "W", "L", "N", "L", "N", "W", \
        "W", "N", "N", "N", "L", "W", "W", "W", "N", "L", "W", "L", "L", "L", \
        "W", "L", "L", "W"]
nulls1 = [6.0, 4.0, 10.0, 8.0, 4.0, 4.0, 6.0, 8.0, 6.0, 4.0, 4.0, 4.0, 10.0, \
        6.0, 4.0, 4.0, 10.0, 4.0, 10.0, 6.0, 4.0, 10.0, 4.0, 6.0, 4.0, 10.0, \
        4.0, 6.0, 4.0, 8.0, 4.0, 6.0, 4.0, 4.0, 10.0, 4.0, 6.0, 8.0, 4.0, 6.0,\
        10.0, 8.0, 4.0, 10.0, 4.0, 8.0, 10.0, 6.0, 4.0, 4.0, 8.0, 4.0, 6.0, 4.0,\
        8.0, 4.0, 4.0, 4.0, 8.0, 4.0]
nulls2 = [4.0, 6.0, 10.0, 6.0, 4.0, 10.0, 4.0, 10.0, 4.0, 8.0, 6.0, 8.0, 6.0,\
        8.0, 4.0, 8.0, 8.0, 4.0, 4.0, 6.0, 4.0, 4.0, 6.0, 4.0, 4.0, 6.0, 4.0, \
        4.0, 8.0, 10.0, 6.0, 4.0, 4.0, 10.0, 6.0, 4.0, 4.0, 10.0, 6.0, 10.0, \
        6.0, 4.0, 10.0, 6.0, 10.0, 4.0, 4.0, 4.0, 4.0, 6.0, 6.0, 6.0, 4.0, 4.0,\
        8.0, 4.0, 4.0, 8.0, 8.0, 4.0]
nulls3 = [8.0, 4.0, 8.0, 4.0, 8.0, 4.0, 8.0, 4.0, 4.0, 4.0, 10.0, 4.0, 6.0, 4.0,\
        6.0, 4.0, 8.0, 6.0, 6.0, 4.0, 4.0, 10.0, 6.0, 4.0, 6.0, 4.0, 10.0, 6.0,\
        6.0, 4.0, 4.0, 8.0, 4.0, 6.0, 4.0, 8.0, 8.0, 4.0, 4.0, 6.0, 10.0, 8.0, \
        8.0, 10.0, 6.0, 4.0, 4.0, 10.0, 4.0, 6.0, 4.0, 10.0, 4.0, 4.0, 4.0, \
        10.0, 6.0, 4.0, 4.0, 10.0]
# generar target-cue e cue-fb isi (2, 4 or 6 secs)
#from random import shuffle
#ISI2durs = [2]*(int(len(seq1)/3)) + [4]*(int(len(seq1)/3)) + [6]*(int(len(seq1)/3))
#shuffle(ISI2durs))
#ISI3durs = [2]*(int(len(seq1)/3)) + [4]*(int(len(seq1)/3)) + [6]*(int(len(seq1)/3))
#shuffle(ISI3durs))
ISI2durs = [2.5, 3.0, 3.0, 2.5, 2.5, 3.0, 2.0, 2.5, 2.5, 2.0, 2.5, 3.0, 2.5, \
            2.0, 2.0, 2.5, 3.0, 3.0, 2.5, 2.0, 2.5, 2.5, 3.0, 3.0, 3.0, 2.0, \
            2.0, 2.5, 3.0, 3.0, 2.0, 3.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.5, 2.5, \
            2.0, 2.0, 3.0, 2.5, 2.5, 2.0, 3.0, 3.0, 3.0, 3.0, 2.5, 2.0, 2.5, \
            2.0, 3.0, 2.0, 2.5, 2.5, 2.0, 3.0, 2.0]
ISI3durs = [2.5, 2.0, 3.0, 2.5, 2.5, 2.0, 2.5, 2.5, 3.0, 2.0, 3.0, 2.5, 2.5, \
            3.0, 2.0, 2.0, 2.5, 2.5, 3.0, 2.0, 2.5, 2.0, 2.5, 2.0, 3.0, 3.0, \
            2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.0, 2.5, 2.5, 2.5, 3.0, 3.0, 2.5, \
            2.0, 2.0, 2.0, 3.0, 3.0, 2.5, 2.0, 3.0, 3.0, 2.5, 2.0, 2.0, 2.0, \
            3.0, 2.5, 2.5, 2.0, 3.0, 2.0, 2.5, 2.0]


# Value returned by the Response pad for each of the buttons
BUTTON_1 = "c"
BUTTON_2 = "d"
BUTTON_3 = "a"

SCAN_TRIGG = 1 #mouse left button


###############################
# Get remaining configuration #
# parameters.                 #
###############################

# Store info about the experiment session
expName = 'MID_Incerteza'  # filename

# gui dialogue to get participant id, goup, and type of sequencia
expInfo = {'ParticipantNumber':'',\
           'Sequencia': [1, 2, 3], \
           'Group': ['control', 'experimental'],
           'Initial Target Duration (in secs)':targetDurationI}

dlg = gui.DlgFromDict(dictionary=expInfo, title=expName, fixed=[])

# if user pressed cancel, quit
if dlg.OK == False:
    core.quit()

# set a few more configuration parameters
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

if type(expInfo['Sequencia'])==int:
    expInfo['Sequencia'] = str(expInfo['Sequencia'])
# Stim Lists
if expInfo['Sequencia'] == '1':
    sequencia = seq1
    nulls = nulls1
elif expInfo['Sequencia'] == '2':
    sequencia = seq2
    nulls = nulls2
elif expInfo['Sequencia'] == '3':
    sequencia = seq3
    nulls = nulls3
targetDurationI = expInfo['Initial Target Duration (in secs)']

################################
# Define some functions #
################################


# function to get mouse clicks
def getMClick(myMouse,mTimeOld,mTimeNew):
    mouse1, mouse2, mouse3 = myMouse.getPressed()
    mouseResp = 0
    if mouse1:
        if mTimeNew-mTimeOld>.4:
            mouseResp = 1
            return mouseResp


# funcion para borrar a cola de respostas
def clear_all_cue():
    while True:
        if event.getKeys(): event.clearEvents()
        else: break


# funcion para recoller as respostas do teclado ou da cedrus
def get_response(BUTTON_1,BUTTON_2, BUTTON_3):
    key_out=[]
    resp = event.getKeys()
    if resp:
        key=resp[0]
        if key==BUTTON_1:key_out=1
        elif key==BUTTON_2:key_out=2
        elif key==BUTTON_3:key_out=3
        elif key=="escape":key_out=99
        return key_out

def staircase(targetDuration,correctResp,nTrials):
    if targetDuration<0.02: newtargetDuration=0.02
    elif (correctResp/nTrials)>.5: newtargetDuration = targetDuration-0.02
    elif (correctResp/nTrials)<.5: newtargetDuration = targetDuration+0.02
    else: newtargetDuration = targetDuration
    return newtargetDuration

#########
# EXCEL #
#########

def saveExcel(Cue_Types,Responses,respTimes, Feedback_Stims,Ideal_Trgt_Durs,Real_Trgt_Durs,StartTime_Cue,StartTime_Target,StartTime_Feedback, TotalMoney):
    df = pd.DataFrame({'1_CueType':Cue_Types,
                       '2_Response':Responses,
                       '3_ReactionTimes':respTimes,
                       '4_FeedbackStim':Feedback_Stims,
                       '5_IdealTargetDuration':Ideal_Trgt_Durs,
                       '6_RealTargetDuration':Real_Trgt_Durs,
                       '7_StartTime_Cue':StartTime_Cue,
                       '8_StartTime_Target':StartTime_Target,
                       '9_StartTime_Feedback':StartTime_Feedback,
                       '10_Money':TotalMoney})
    writer = ExcelWriter('data' + os.path.sep + '%s_%s.xlsx' %(expInfo['ParticipantNumber'], expInfo['date']))
    df.to_excel(writer,'Sheet1',index=False)
    writer.save()


################
# Output files #
################

# Setup files for saving
if not os.path.isdir('data'):
    # if this fails (e.g. permissions) we will get error
    os.makedirs('data')

filename = 'data' + os.path.sep + '%s_%s_%s' %(expInfo['ParticipantNumber'],expInfo['Group'],expInfo['date'])



#####################
# Setup the Window. #
#####################

win = visual.Window(size=(800, 768),
                    fullscr=FULL_SCREEN,
                    screen=0,
                    allowGUI=False,
                    allowStencil=False,
                    monitor='testMonitor',
                    color='black',
                    colorSpace='rgb',
                    units='norm')



#########################################
# Initialize various display components #
#########################################



# fixation

cueWin = visual.ImageStim(win, image='stims'+ os.path.sep + 'Cue_win.bmp', pos=(0,0))
cueNeu = visual.ImageStim(win, image='stims'+ os.path.sep + 'Cue_neu.bmp', pos=(0,0))
cueLos = visual.ImageStim(win, image='stims'+ os.path.sep + 'Cue_los.bmp', pos=(0,0))
target = visual.ImageStim(win, image='stims'+ os.path.sep + 'Target.bmp', pos=(0,0)) #size=[0.6, 0.6]

fbWin = visual.TextStim(win=win, name='win', text=u'0,10€', font='Arial', pos=[0,0], height=0.18, wrapWidth=1, color='green')
fbNeu = visual.TextStim(win=win, name='neu', text=u'0,00€', font='Arial', pos=[0,0], height=0.18, wrapWidth=1, color='white')
fbLos = visual.TextStim(win=win, name='los', text=u'-0,10€', font='Arial', pos=[0,0], height=0.18, wrapWidth=1, color='red')
fbTotal = visual.TextStim(win=win, name='total', text=u'0,00€', font='Arial', pos=[0,-.5], height=0.1, wrapWidth=1, color='white')
fixation = visual.ShapeStim(win,units='cm',
    lineWidth=6, vertices=((-0.7, 0), (0.7, 0), (0,0), (0,0.7), (0,-0.7)),
    interpolate=True, closeShape=False, pos=(0,0), lineColor='white')

instru_text = visual.TextStim(win=win, name='instruct', text= u'Comenzamos en breve', height=0.15, wrapWidth=1.8, color='white')
comenzamos = visual.TextStim(win=win, name='begin', text= u'Comenzamos', height=0.15, wrapWidth=1.8, color='white')
thanks = visual.TextStim(win=win, ori=0, name='thanks', text='Gracias',height=0.15, wrapWidth=1,color='white')


########################
# Start the experiment #
########################

# Initialize timers
globalClock = core.Clock()  # to track the time since experiment started
globalClock2 = core.Clock()
trialClock = core.Clock()

# Initialize mouse
myMouse = event.Mouse(visible=False)


instru_text.draw()
win.flip()


nTrial = 0 # suma solo trials non neutros (win o loose)
nResponses = 0
targetDurationF = targetDurationI
targetDurationV = targetDurationI
Cue_Types = []
Responses = []
Feedback_Stims = []
Ideal_Trgt_Durs = []
Real_Trgt_Durs =[]
StartTime_Cue = []
StartTime_Target = []
StartTime_Feedback = []
respTimes =[]
TotalMoney =[]
##########################
# wait for scan triggers #
##########################
clear_all_cue()
oldMClock = 0
mouseResp = None
while not mouseResp:
    mouseResp = getMClick(myMouse,0,1)

globalClock.reset()

comenzamos.draw()
win.flip()
while globalClock.getTime()<7.5: # wait 4 TR for scan stabilization
    core.wait(0.01)

totalTime = 8 # change for the seconds of waiting after first scan trigg



for idx,trial in enumerate(sequencia):
    ISI1dur = nulls[idx]
    ISI2dur = ISI2durs[idx] - targetDurationF # OJO a este ISI restamoslle target duration
    ISI3dur = ISI3durs[idx]
    #fixation 1
    fixation.draw()
    while globalClock.getTime()<totalTime-0.015:
        core.wait(0.002)
    win.flip()
    totalTime = totalTime+ISI1dur

    # define and show cue
    if trial == "W":
        cueWin.draw()
        targetDurationF = targetDurationV
    elif trial == "N":
        cueNeu.draw()
        targetDurationF = targetDurationI
    else:
        cueLos.draw()
        targetDurationF = targetDurationV
    while globalClock.getTime()<totalTime-0.015:
        core.wait(0.002)
    win.flip()
    StartTime_Cue.append(globalClock.getTime())
    totalTime = totalTime + cueDuration

    # fixation 2
    Cue_Types.append(trial)
    fixation.draw()
    while globalClock.getTime()<totalTime-0.015:
        core.wait(0.002)
    win.flip()
    totalTime = totalTime + ISI2dur

    # show target
    target.draw()
    responded = False
    respondedOK = False
    clear_all_cue()
    while globalClock.getTime()<totalTime-0.015:
        if not responded:
            resp = get_response(BUTTON_1,BUTTON_2, BUTTON_3)
            if resp:
                respTimes.append(globalClock.getTime())
                Responses.append("TooFast")
                responded = True
    win.flip()
    trialClock.reset()
    StartTime_Target.append(globalClock.getTime())
    totalTime = totalTime + targetDurationF

    ## get response during target
    fixation.draw()
    while globalClock.getTime()<totalTime-0.014:
        if not responded:
            resp = get_response(BUTTON_1,BUTTON_2, BUTTON_3)
            if resp:
                respTimes.append(trialClock.getTime())
                Responses.append("OK")
                responded = True
                respondedOK = True
    win.flip()
    Real_Trgt_Durs.append(trialClock.getTime())
    # fixation 3 target-fb (and get late responses)
    totalTime = totalTime + ISI3dur
    while globalClock.getTime()<totalTime-0.1:
        if not responded:
            resp = get_response(BUTTON_1,BUTTON_2, BUTTON_3)
            if resp:
                respTimes.append(trialClock.getTime())
                Responses.append("LATE")
                responded = True


    ## update target time
    Ideal_Trgt_Durs.append(targetDurationF)
    if respondedOK: nResponses += 1
    if trial != "N":
        nTrial += 1
        targetDurationV = staircase(targetDurationV,nResponses,nTrial)
        targetDurationF = targetDurationV

    if not responded:
        Responses.append("NO")
        respTimes.append(None)
    # show feedback
    if trial == "W" and respondedOK:
        fbWin.draw()
        Feedback_Stims.append("Won")
        Money +=0.1
    elif trial == "W" and not respondedOK:
        fbNeu.draw()
        Feedback_Stims.append("None")
    elif trial == "L" and respondedOK:
        fbNeu.draw()
        Feedback_Stims.append("None")
    elif trial == "L" and not respondedOK:
        fbLos.draw()
        Feedback_Stims.append("Lose")
        Money -=0.1
    else:
        fbNeu.draw()
        Feedback_Stims.append("None")
    TotalMoney.append(Money)
    while globalClock.getTime()<totalTime-0.015:
        core.wait(0.02)
        resp = get_response(BUTTON_1,BUTTON_2, BUTTON_3)
        if resp == 99:
            StartTime_Feedback.append('__')
            saveExcel(Cue_Types,Responses,respTimes,Feedback_Stims,Ideal_Trgt_Durs,Real_Trgt_Durs,StartTime_Cue,StartTime_Target,StartTime_Feedback, TotalMoney)
            win.close()
            core.quit()

    Money = round(Money,2)
    fbTotal.setText(str(Money) + '€')
    fbTotal.draw()

    win.flip()
    StartTime_Feedback.append(globalClock.getTime())
    totalTime = totalTime + fbDuration

    # fixation 4
######### temporalmente quitamos ISI entre fbparcial e fbtotal ############
#    fixation.draw()
#    while globalClock.getTime()<totalTime-0.015:
#        core.wait(0.002)
#    win.flip()
#    totalTime = totalTime + ISI4dur

    # global feedback

    while globalClock.getTime()<totalTime-0.015:
        core.wait(0.02)
        resp = get_response(BUTTON_1,BUTTON_2, BUTTON_3)
        if resp == 99:
            saveExcel(Cue_Types,Responses,respTimes,Feedback_Stims,Ideal_Trgt_Durs,Real_Trgt_Durs,StartTime_Cue,StartTime_Target,StartTime_Feedback, TotalMoney)
            win.close()
            core.quit()
    #win.flip()
    totalTime = totalTime + TfbDuration

fixation.draw()
win.flip()
saveExcel(Cue_Types,Responses,respTimes,Feedback_Stims,Ideal_Trgt_Durs,Real_Trgt_Durs,StartTime_Cue,StartTime_Target,StartTime_Feedback, TotalMoney)
core.wait(8)
thanks.draw()
win.flip()

core.wait(4)
win.close()
core.quit()
