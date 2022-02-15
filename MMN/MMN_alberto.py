#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sound task (to run in Psychopy v3.07)
"""
from psychopy import visual, core, data, event, gui, sound, parallel
from psychopy.sound import backend_pygame
import os, sys
from numpy.random import random, shuffle, choice
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile



# Turn fullscreen off for testing on monitor
FULL_SCREEN = False


minISI = .5
maxISI = .7

#tada = sound.backend_sounddevice.SoundDeviceSound(os.getcwd() + os.path.sep + 'AUDIO02.wav')
#ding = sound.Sound(os.getcwd() + os.path.sep + 'AUDIO13.wav')
#tada = sound.backend_pygame.SoundPygame(os.getcwd() + os.path.sep + 'AUDIO02.wav')

standard = backend_pygame.SoundPygame(os.getcwd() + os.path.sep + 'std.wav')
deviant = backend_pygame.SoundPygame(os.getcwd() + os.path.sep + 'dev.wav')

# No usado
rest_instructions = u'Descanso.\n\nPreme a barra espaciadora para continuar'
thanks_text = u'Obrigado'
# #####

# ###############
# crear stims (504 standar, 96 desviantes) (96*5=480 standar de relleno;24 standar non relleno)
#sounds1 = ([1]*96)+([0]*24)
#shuffle(sounds1)
#soundsList = []
#for i in sounds1:
#    if i:
#        soundsList.extend([1,0,0,0,0,0])
#    else:soundsList.append(0)
# ###############

# ###############
# crear stims (504 standar, 96 desviantes) (96*4=384 standar de relleno;120 standar non relleno)
sounds1 = ([1]*96)+([0]*120)
shuffle(sounds1)
soundsList = []
for i in sounds1:
    if i:
        soundsList.extend([1,0,0,0,0])
    else:soundsList.append(0)
# ###############


def send_trigger(code,parallel_port,parallel):
    if parallel_port == 1:
        parallel.setData(code)
        core.wait(.005)
        parallel.setData(0)
    else:
        pass

# clear response queue
def clear_all_queue():
    while True:
        if event.getKeys(): event.clearEvents('keyboard')
        else: break

# get response from cedrus, or the keyboard in its absence
def get_response():
    key_out=[]
    resp=event.getKeys()
    if resp:
        key=resp[0]
        if key=='space':key_out=9#code that sends for spacebar
        elif key=="escape":key_out=99
        return key_out

def saveExcel(ntrials,stimTypes,stimTimes):
    df = pd.DataFrame({'1_Trial':ntrials,
                       '2_StimType':stimNames,
                       '3_StimTime':stimTimes
                       })
    writer = ExcelWriter('MMN_data' + os.path.sep + '%s_%s.xlsx' %(expInfo['ID Participant'], expInfo['date']))
    df.to_excel(writer,'Sheet1',index=False)
    writer.save()

def showInstructs(image_path):
    picture.setImage(image_path)
    picture.draw()
    win.flip()
    core.wait(.5)
    clear_all_queue()
    while True:
        resp = get_response()
        core.wait(.01)
        if resp==9:
            break

#parallel port setup
try:
    parallel.setPortAddress(0x378)#direccion do porto paralelo
    parallel.setData(0)
    parallel_port=1
except:
    parallel_port=0
    print("Oops!  No parallel port found")

# Store info about the experiment session
expName = 'MMN'
expInfo = {'ID Participant':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName, fixed=[])
if dlg.OK == False:
    core.quit()
expInfo['date'] = data.getDateStr()  # timestamp
expInfo['expName'] = expName
if not os.path.isdir('MMN_data'):
    os.makedirs('MMN_data')

# Setup the Window
win = visual.Window(size=(800, 768), fullscr=FULL_SCREEN, units='norm')
instruct_text = visual.TextStim(win=win, text=rest_instructions, height=0.1, wrapWidth=1.5, color='white')


ntrials = range(1,len(soundsList)+1)
stimNames = [None]*len(soundsList)
tTimesS = [None]*len(soundsList)

# Initialize timers
globalClock = core.Clock()  # to track the time since experiment started
trialClock = core.Clock()
ISIClock = core.Clock()


for idx, sound in enumerate(soundsList):
    trialClock.reset()
    if sound == 0:
        durat = standard.getDuration()
        standard.play()
    else:
        durat = deviant.getDuration()
        deviant.play()

    send_trigger(sound+100,parallel_port,parallel)
    tTimesS[idx]=globalClock.getTime()

    while trialClock.getTime()<durat: # trialClock.getTime()<durat+isi if you want to add isi
        core.wait(.002)
    # ISI
    ISIClock.reset()
    ISI = minISI+random()*(maxISI-minISI)

    if sound == 1:
        stimNames[idx]='dev'
    else: stimNames[idx]='std'

    while ISIClock.getTime()<ISI:
        resp = get_response()
        if resp == 99:
            saveExcel(ntrials,stimNames,tTimesS)
            win.close()
            core.quit()
        core.wait(.002)


# thanks and save
#picture.setImage('Instructions'+ os.path.sep + 'Instruction.9.jpeg')
#picture.draw()
win.flip()
saveExcel(ntrials,stimNames,tTimesS)
core.wait(3)
win.close()
core.quit()
