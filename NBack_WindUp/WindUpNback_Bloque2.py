#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from psychopy import core, data, event, visual, gui, parallel, sound
import serial, time, random, os, pyxid
from itertools import cycle
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


FULL_SCR = True
STIM_DUR = 0.5
# task instructions
instructionsBegin = u'Press "enter" to begin'
instructionsBreak = u'Break. Press enter to continue'
instructionsText1 = u'Evalúa el dolor'
instructionsHand = u'Responde con la mano '


tick = sound.Sound(800,secs=1.6)
###############################
# Get remaining configuration #
# parameters.                 #
###############################

# Store info about the experiment session
expName = 'TCS_WM_Bloque2'  # filename

# gui dialogue to get participant id, goup, and type of sequencia
expInfo = {'ParticipantNumber':''}

dlg = gui.DlgFromDict(dictionary=expInfo, title=expName, fixed=[])

# if user pressed cancel, quit
if dlg.OK == False:
    core.quit()

# set a few more configuration parameters
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

if int(expInfo['ParticipantNumber'])%4 == 0:
    blocks = ['0P', '2P', 'WU', 'WM', '2P', 'WU', 'WM', '0P', 'WU', 'WM', '0P', '2P', 'WM', '0P', '2P', 'WU', '0P', '2P', 'WU', 'WM']
elif int(expInfo['ParticipantNumber'])%4 == 1:
    blocks = ['WM', 'WU', '2P', '0P', 'WU', '2P', '0P', 'WM', '2P', '0P', 'WM', 'WU', '0P', 'WM', 'WU', '2P', 'WM', 'WU', '2P', '0P']
elif int(expInfo['ParticipantNumber'])%4 == 2:
    blocks = ['2P', '0P', 'WM', 'WU', '0P', 'WM', 'WU', '2P', 'WM', 'WU', '2P', '0P', 'WU', '2P', '0P', 'WM', '2P', '0P', 'WM', 'WU']
elif int(expInfo['ParticipantNumber'])%4 == 3:
    blocks = ['WU', 'WM', '0P', '2P', 'WM', '0P', '2P', 'WU', '0P', '2P', 'WU', 'WM', '2P', 'WU', 'WM', '0P', 'WU', 'WM', '0P', '2P']
hands = cycle(["IZQUIERDA","DERECHA"])

win = visual.Window(size=(600, 600),fullscr=FULL_SCR,screen=0, allowGUI=False,allowStencil=False,
                    monitor='testMonitor',color='black',colorSpace='rgb')

#tick = sound.Sound(800, secs=0.01, sampleRate=44100, stereo=True)  # test
fixation = visual.ShapeStim(win,lineWidth=6,vertices=((-0.05, 0), (0.05, 0), (0,0), (0,0.08), (0,-0.08)), interpolate = False, closeShape=False)
stimWM = visual.TextStim(win=win, text='number',font='Arial',height=0.4, wrapWidth=1.8)
instruct = visual.TextStim(win=win,text= instructionsText1,font='Arial',
                          height=0.1, wrapWidth=1.8, color='white',alignHoriz='center',pos=(0.0, 0.5))
instructHand = visual.TextStim(win=win,text= instructionsHand,font='Arial',
                          height=0.1, wrapWidth=1.8, color='white',alignHoriz='center',pos=(0.0, 0.0))
reminder = visual.TextStim(win=win,text= 'X',font='Arial',
                          height=0.07, wrapWidth=1.8, color='white',alignHoriz='center',pos=(0.0, 0.8))
mouse = event.Mouse(visible=False, newPos=None, win=win)
#ser = serial.Serial('dev/cu.usbmodem1421', 115200)
try:
    ser = serial.Serial('/dev/cu.usbmodem14201', 115200)
except:
    ser=False
    print("Oops! Serial port not found")

#parallel port setup
try:
    parallel.setPortAddress(0x378)#direccion do porto paralelo
    parallel.setData(0)
    parallel_port=True
except:
    parallel_port=False
    print("Oops!  No parallel port found")

#Caixa de respostas cedrus.
try:
    devices = pyxid.get_xid_devices()
    dev = devices[0] # a caixa de respostas sera "dev"
    if dev.is_response_device():
        dev.reset_base_timer()
        dev.reset_rt_timer()
    dev.clear_response_queue()
    cedrus=True
    print("Cedrus response box found! Maybe you need to change the response keys")

except:
    print("No cedrus response box found, we will use the keyboard")
    cedrus=False
    dev=None

#########
# EXCEL #
#########
blcks = []
stimNs = []
stimTypes = []
stimTimes = []
StimDurs = []
RTs = []
TCSStims = []
TCSStimTs = []
TrigsSent = []
VAS1Rates = []
VAS2Rates = []
def excel_append(typeS):
    global blcks
    global stimNs
    global stimTypes
    global stimTimes
    global StimDurs
    global RTs
    global TCSStims
    global TCSStimTs
    global TrigsSent
    global VAS1Rates
    global VAS2Rates
    if typeS=='TCS':
        blcks.append(block)
        stimNs.append(None)
        stimTypes.append('heat')
        stimTimes.append(TCSstimtime)
        StimDurs.append(None)
        RTs.append(None)
        TCSStims.append(hand)
        TCSStimTs.append(TCSstimtime)
        TrigsSent.append(TCS_trigger)
        VAS1Rates.append(None)
        VAS2Rates.append(None)
    elif typeS=='stim':
        blcks.append(block)
        stimNs.append(stimuliNow)
        stimTypes.append('WMStim')
        stimTimes.append(WMstimtime)
        StimDurs.append(TCSstimDur )
        RTs.append(None)
        TCSStims.append(None)
        TCSStimTs.append(None)
        TrigsSent.append(TriggerStim)
        VAS1Rates.append(None)
        VAS2Rates.append(None)
    elif typeS=='resp':
        blcks.append(block)
        stimNs.append(None)
        stimTypes.append('resp')
        stimTimes.append(None)
        StimDurs.append(None)
        RTs.append(resp_time)
        TCSStims.append(None)
        TCSStimTs.append(None)
        TrigsSent.append(99)
        VAS1Rates.append(None)
        VAS2Rates.append(None)
    elif typeS=='vas1':
        blcks.append(block)
        stimNs.append(None)
        stimTypes.append('vas1')
        stimTimes.append(globalClock.getTime())
        StimDurs.append(None)
        RTs.append(None)
        TCSStims.append(None)
        TCSStimTs.append(None)
        TrigsSent.append(None)
        VAS1Rates.append(rating1)
        VAS2Rates.append(None)
    elif typeS=='vas2':
        blcks.append(block)
        stimNs.append(None)
        stimTypes.append('vas2')
        stimTimes.append(globalClock.getTime())
        StimDurs.append(None)
        RTs.append(None)
        TCSStims.append(None)
        TCSStimTs.append(None)
        TrigsSent.append(None)
        VAS1Rates.append(None)
        VAS2Rates.append(rating2)

def saveExcel():
    df = pd.DataFrame({'1_Block':blcks,
                       '2_Stim':stimNs,
                       '3_StimType':stimTypes,
                       '4_StimTime':stimTimes,
                       '5_StimDuration':StimDurs,
                       '6_ResponseTime':RTs,
                       '7_TCS_Stim':TCSStims,
                       '8_TCS_StimTime':TCSStimTs,
                       '9_Trigger':TrigsSent,
                       '10_VAS1_rating':VAS1Rates,
                       '11_VAS2_rating':VAS2Rates})
    writer = ExcelWriter('data' + os.path.sep + '%s_%s_Bloque2.xls' %(expInfo['ParticipantNumber'], expInfo['date']))
    df.to_excel(writer,'Bloque2',index=False)
    writer.save()
# Setup files for saving
if not os.path.isdir('data'):
    # if this fails (e.g. permissions) we will get error
    os.makedirs('data')


#def send_data(data_out): # send by serial
#    if ser!=False:
#        for i in data_out:
#            ser.write(i.encode())
#            time.sleep(0.002)
def read_data(): # read serial
    if ser!=False:
        incoming=''
        while ser.inWaiting():
            incoming = incoming + ser.read().decode()
        return(incoming)

# functions for responses
def clear_all_cue():
    if cedrus:
        while True:
            dev.poll_for_response()
            if dev.response_queue_size():
                dev.clear_response_queue()
            else: break
    else:
        while True:
            if event.getKeys(): event.clearEvents('keyboard')
            else: break

def get_response():
    key_out=[]
    if cedrus:
        dev.poll_for_response()
        if dev.response_queue_size()>0:
            resp = dev.get_next_response()
            if resp['pressed']==True:
                #key = resp['key']
                key = 1
                return key
        else:
            resp=event.getKeys()
            if resp:
                if resp[0]=='escape':key_out=99
                return key_out
    else:
        resp=event.getKeys()
        if resp:
            key=resp[0]
            if key=='space':key_out=1
            elif key=="escape":key_out=99
            return key_out

def send_trigger(code):
    if parallel_port == 1:
        parallel.setData(code)
        core.wait(.005)
        parallel.setData(0)
    else:
        pass
def pain_rate(vasNum):
    event.Mouse(visible = True)
    instruct.setText(instructionsText1)
    ratingScale1 = visual.RatingScale(win, low=0, high=10,precision=10,showValue =False,acceptText='Aceptar',
                                            labels=['Nada doloroso', 'Dolor insoportable'], size=1.5,
                                            scale='0                                                10',
                                            acceptPreText='Aceptar')
    if  vasNum==1:
        send_trigger(50)
        core.wait(0.3+random.random()*0.5)
        if TCS_trigger>0:
            send_trigger(TCS_trigger)
            TCSstimtime = globalClock.getTime()
            excel_append('TCS')
    elif vasNum ==2:
        send_trigger(51)
        core.wait(0.3+random.random()*0.5)
        if TCS_trigger>0:
            send_trigger(TCS_trigger+1)
            TCSstimtime = globalClock.getTime()
            excel_append('TCS')
    while ratingScale1.noResponse:
                resp = get_response()
                ratingScale1.draw()
                instruct.draw()
                win.flip()
    rating1temp = ratingScale1.getRating()
    win.flip()
    event.Mouse(visible = False)
    return(rating1temp)

def back2():
    lista = []
    idxsr = []
    nTarget = random.choice([2,3,3,3,4,4])
    idxs = random.sample(range(2,10),nTarget)
    for i in range(10):
        if i in idxs:
            lista.append(lista[i-2])
            idxsr.append(10)
        else:
            if len(lista)<2: lista.append(random.choice(range(10)))
            else:
                x = list(range(10))
                x.remove(lista[i-2])
                lista.append(random.choice(x))
            idxsr.append(0)
    return(lista,idxsr)

def back1():
    lista = []
    idxsr = []
    nTarget = random.choice([2,3,3,3,4,4])
    idxs = random.sample(range(2,10),nTarget)
    for i in range(10):
        if i in idxs:
            lista.append(lista[i-1])
            idxsr.append(10)
        else:
            if len(lista)<2: lista.append(random.choice(range(10)))
            else:
                x = list(range(10))
                x.remove(lista[i-1])
                lista.append(random.choice(x))
            idxsr.append(0)
    return(lista,idxsr)

def back0():
    lista = []
    nTarget = random.choice([2,3,3,3,4,4])
    idxs = random.sample(range(2,10),nTarget)
    idxsr = []
    for i in range(10):
        if i in idxs:
            lista.append('X')
            idxsr.append(10)
        else:
            lista.append(random.choice(range(10)))
            idxsr.append(0)
    return(lista,idxsr)

def heatTimes():
    times = []
    ttimes = []
    for i in range(10):
        times.append(random.random()*0.8+2.5)
        ttimes.append(33-sum(times))
    ttimes.sort()
    return(ttimes)

def numTimes(heatTimesV):
    tlim = heatTimesV[-1]-random.random()*0.8
    while True:
        times = []
        ttimes = []
        for i in range(10):
            times.append(random.random()*0.8+2.5)
            ttimes.append(31-sum(times))
        if ttimes[-1]>0 and ttimes[-1]<0.5:
            ttimes.sort()
            return(ttimes)
            break
########################## TCS conection
#time.sleep(1)
#print(read_data())
#time.sleep(.5)
#send_data('S10001') # activar todas as superficies
#time.sleep(.1)
#send_data('C0090') #Setting the temperature setpoint
#time.sleep(.1)
#send_data('G') #authomatic calibration
#time.sleep(5)
#send_data('N420') #Setting resting temp N230
#time.sleep(.1)
#send_data('D001000') #Setting the stimulation time (Ds00200 = 200ms)
#time.sleep(.1)
#send_data('T255010') #Set trigger and duration
#time.sleep(.1)
#send_data('P') # ask for parameter
#time.sleep(.1)
#print(read_data())
#send_data('E') # ask for temperatures
#time.sleep(.1)
#print(read_data())
########################

globalClock = core.Clock()
blockClock = core.Clock()
stimClock = core.Clock()
TCSstimtime = globalClock.getTime()
for block in blocks:
    hand = hands.next() # seleccionar man de sujetar. Cambiar en todos os bloques? ou solo nos de stim?
    if block == '0P':
        tri = back0()
        trials = tri[0]
        idx_trig = tri[1]
        instructHand.setText('0-back (RESPONDE A LA "X")\n\nSujeta el estimulador con la mano ' + hand+ '\n\nHaz click para comenzar')
        reminder.setText('Responde X')
        TCS_trigger = 128
        WM_trigger = 11
    elif block == '2P':
        tri = back2()
        trials = tri[0]
        idx_trig = tri[1]
        instructHand.setText('2-BACK\n\nSujeta el estimulador con la mano ' + hand+ '\n\nHaz click para comenzar')
        reminder.setText('2 Back')
        TCS_trigger = 129
        WM_trigger = 12
    elif block == 'WU':
        trials = ['X']*10
        idx_trig = [0]*10
        instructHand.setText('ATIENDE A TU MANO\n\nSujeta el estimulador con la mano ' + hand+ '\n\nHaz click para comenzar')
        reminder.setText('Mano')
        TCS_trigger = 130
        WM_trigger = 13
    elif block == 'WM':
        tri = back2()
        trials = tri[0]
        idx_trig = tri[1]
        instructHand.setText('2-BACK\n\nSujeta el estimulador con la mano ' + hand+ '\n\nHaz click para comenzar')
        reminder.setText('2 Back')
        TCS_trigger = 0
        WM_trigger = 14
    heatStimT = heatTimes()
    numStimT = numTimes(heatStimT)
    # show instructions
    reminder.setAutoDraw(True)
    instructHand.draw()
    win.flip()
    core.wait(2)
    while sum(mouse.getPressed())==0:
        core.wait(.1)
    fixation.draw()
    win.flip()
    core.wait(random.random()+1)
    # first thermal stim and rate
#    send_data('L')
    rating1 = pain_rate(1)
    excel_append('vas1')
    fixation.draw()
    win.flip()
    core.wait(random.random()*0.8+0.5)
    blockClock.reset()
    WMtrial = 0
    Heattrial = 0
    stimShown = False
    WMstimtime = 0
    WMstimDur = 0
    TCSstimtime = 0
    respondeu = False
    while Heattrial<10:
        if WMtrial<10:
            if blockClock.getTime()>numStimT[WMtrial]:
                stimuliNow = str(trials[WMtrial])
                stimWM.setText(stimuliNow)
                if block!= "WU":
                    stimWM.draw()
                    win.flip()
                WMstimtime =globalClock.getTime()
                stimClock.reset()
                TriggerStim = WM_trigger+idx_trig[WMtrial]
                send_trigger(TriggerStim)
                respondeu = False
                stimShown = True
                WMtrial +=1
                clear_all_cue()
        if blockClock.getTime()>heatStimT[Heattrial]:
            Heattrial +=1
            #send_data('L')
            if TCS_trigger>0:
                TCSstimtime = globalClock.getTime()
                send_trigger(TCS_trigger)
                excel_append('TCS')

        if stimClock.getTime()>STIM_DUR-0.01 and stimShown:
            fixation.draw()
            win.flip()
            TCSstimDur = globalClock.getTime()
            stimShown=False
            excel_append('stim')
        if not respondeu:
            resposta = get_response()
            if resposta:
                resp_time = stimClock.getTime()
                send_trigger(99)
                excel_append('resp')
                respondeu = True
                if resposta == 99:
                    saveExcel()
                    win.close()
                    core.quit()
    core.wait(2.2+random.random()*.6)
    reminder.setAutoDraw(False)
    rating2 = pain_rate(2)
    excel_append('vas2')
    fixation.draw()
    win.flip()
    core.wait(random.random()*0.8+0.5)

saveExcel()
win.close()
core.quit()
if ser!=False:
    ser.close()
