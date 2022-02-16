#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Anxiety task (to run in Psychopy v3.07)
"""
from psychopy import visual, core, data, event, gui, sound, parallel
import os, sys
from numpy.random import random, shuffle, choice
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
#import pyxid

# times

STIM_TIME = 1.5 #stim duration
ISI_TIME = 1.5 # interstimulus interval

# Valor que envía o lumina ao pulsar o botón esquerdo ou dereito
LUMINA_LEFT = 0
LUMINA_RIGHT = 2
# Turn fullscreen off for testing on monitor
FULL_SCREEN = True


t=['t']*25 #triangulo
c=['c']*35 #circulo
d=['d']*35 #cuadrado
m=['m']*12 #medo
blocks = t+c+d+m
shuffle(blocks)
#while True:
#    shuffle(blocks)
#    repeat = False
#    for idx, i in enumerate(blocks):
#        if idx>0:
#            if blocks[idx]==blocks[idx-1]:
#                repeat = True
#    if not repeat:
#        break
#    

# Caixa de respostas cedrus.
try:
   devices = pyxid.get_xid_devices()
   dev = devices[0] # a caixa de respostas sera "dev"
   if dev.is_response_device():
       dev.reset_base_timer()
       dev.reset_rt_timer()
   dev.clear_response_queue()
   cedrus=1
   print("Cedrus response box found! Maybe you need to change the response keys (see line 21-22)")

except:
   print ("No cedrus response box found, we will use the keyboard")
   cedrus=0
   dev=None

#parallel port setup
try:
    parallel.setPortAddress(0x378)#direccion do porto paralelo
    parallel.setData(0)
    parallel_port=1
except:
    parallel_port=0
    print("Oops!  No parallel port found")

# funcion para recoller as respostas do teclado ou da cedrus
def get_response(cedrus,dev,luminaL,luminaR):
  key2=[]
  if cedrus:
      dev.poll_for_response()
      if dev.response_queue_size()>0:
          resp = dev.get_next_response()

          if resp['pressed']==True:
            key=resp['key']
            if key==luminaL:
                key2=1
            elif key==luminaR:
                key2=2
            return key2
      else:
          resp=event.getKeys()
          if resp:
              if resp[0]=='escape':key2=99
              if resp[0]=='return':key2=98
              return key2
  else:
      resp=event.getKeys()
      if resp:
          key=resp[0]
          if key=='m':key2=1
          if key=='z':key2=2
          if key=='return':key2=98
          elif key=="escape":key2=99
          return key2


# clear response queue
def clear_all_queue():
    while True:
        if event.getKeys(): event.clearEvents('keyboard')
        else: break

# get responses from the cedrus lumina fMRI controller (in keyboard mode)
def send_trigger(code,parallel_port,parallel):
    if parallel_port == 1:
        parallel.setData(code)
        core.wait(.005)
        parallel.setData(0)
    else:
        pass

def clear_all_queue():
    while True:
        if event.getKeys(): event.clearEvents('keyboard')
        else: break

def saveExcel(ntrials,stimTypes,stimTimes, resps, rts, VasVals):
    df = pd.DataFrame({'1_ntrial':ntrials,
                       '2_stimType':stimTypes,
                       '3_stimTimes':stimTimes,
                       '4_response':resps,
                       '5_respTimes':rts,
                       '6_VasValue':VasVals})
    writer = ExcelWriter('data' + os.path.sep + '%s_%s.xlsx' %(expInfo['ParticipantNumber'], expInfo['date']))
    df.to_excel(writer,'Sheet1',index=False)
    writer.save()


def showScale():
    message= visual.TextStim(win, text="Por favor, evalúe su nivel de ansiedad", height = .1)
    scale = visual.RatingScale(win, labels=['Nada', 'Extremo'], scale=None,low=1, high=100, tickHeight=1)
    while scale.noResponse:
        scale.draw()
        message.draw()
        win.flip()
    return scale.getRating()
    


# Initialize timers
globalClock = core.Clock()  # to track the time since experiment started
trialClock = core.Clock()

# control trials presentation and data to save
n_trial = 1
ntrials = []
stimTypes = []
stimTimes = []
resps = []
rts = []
VasVals = []

def trial_counter(typeEv, timeSt, rt, resp, vas_val):
    global n_trial
    global ntrials
    n_trial += 1
    ntrials.append(n_trial)
    stimTypes.append(typeEv)
    stimTimes.append(timeSt)
    resps.append(resp)
    rts.append(rt)
    VasVals.append(vas_val)

# Store info about the experiment session
expName = 'anxiety'
# gui dialogue to get participant id
expInfo = {'ParticipantNumber':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName, fixed=[])
# if user pressed cancel, quit
if dlg.OK == False:
    core.quit()
# more configuration parameters
expInfo['date'] = data.getDateStr()  # timestamp
expInfo['expName'] = expName

# Setup files for saving
if not os.path.isdir('data'):
    os.makedirs('data')



# Setup the Window
win = visual.Window(size=(800, 768), fullscr=FULL_SCREEN, units='norm', color = 'black')
# display components
cuad = visual.ImageStim(win, image= 'Cuad.png')
circ = visual.ImageStim(win, image= 'Circ.png')
tria = visual.ImageStim(win, image= 'Tria.png')
medo = visual.ImageStim(win, image= 'Pic.jpg', size = 2, units = 'norm')
S1 = sound.backend_sounddevice.SoundDeviceSound(os.getcwd() + os.path.sep + 'Fear1.wav')


event.Mouse(visible=False)




# task starts
totalTime = 0

clear_all_queue()
m1= visual.TextStim(win, text="Pulsa cuando veas el triángulo. \nPulsa un botón para comenzar", height = .1)
m1.draw()
win.flip()
while True:
    resp = get_response(cedrus,dev,LUMINA_LEFT,LUMINA_RIGHT)
    if resp:
        if resp:
            globalClock.reset()
            trialClock.reset()
            break

win.flip()

for Bidx,block in enumerate(blocks):
    # ISI
    if block == 't': # triangulo
        tria.draw()
        win.flip()
        send_trigger(1,parallel_port,parallel)
    elif block == 'c': # circulo
        circ.draw()
        win.flip()
        send_trigger(2,parallel_port,parallel)
    elif block == 'd': # cuadrado
        cuad.draw()
        win.flip()
        send_trigger(3,parallel_port,parallel)
    elif block == 'm': # medo
        medo.draw()
        S1.play()
        win.flip()
        send_trigger(9,parallel_port,parallel)
        
    stimTime = globalClock.getTime()
    trialClock.reset()
    responded = False
    blackScreen = False
    while trialClock.getTime()<STIM_TIME+ISI_TIME:
        core.wait(.002)
        if trialClock.getTime()>STIM_TIME and blackScreen == False:
            blackScreen = True
            win.flip()
        if not responded:
            resp = get_response(cedrus,dev,LUMINA_LEFT,LUMINA_RIGHT)
            if resp == 1 or resp == 2:
                rt = trialClock.getTime()
                send_trigger(99,parallel_port,parallel)
                responded = True
            elif resp == 99:
                saveExcel(ntrials,stimTypes,stimTimes, resps, rts, VasVals)
                win.close()
                core.quit()
                        
#        trial_counter('stim', globalClock.getTime(), stimName = block, otherstimName = 'none', stimType = 'rest', stimBlock = 'rest', tTimesISi = 'none')
    if responded:
        vas = None
        trial_counter(block, stimTime, rt, resp, vas)
    else:
        rt = None
        resp = None
        vas = None
        trial_counter(block, stimTime, rt, resp, vas)
        
    # presentar vas
    if Bidx == 53:
        stimTime = globalClock.getTime()
        vas_val = showScale()
        rt = None
        resp = None
        trial_counter('vas', stimTime , rt, resp, vas_val)
        event.Mouse(visible=False)
        win.flip()
        core.wait(1.9)

saveExcel(ntrials,stimTypes,stimTimes, resps, rts, VasVals)

win.flip()
win.close()
core.quit()
