#Anna Gaglianese March 2022

import os
import pickle
import numpy as np
import random
import psychopy.gui
import psychopy.event
import psychopy.core
import psychopy.visual
from psychopy.hardware import keyboard
import psychopy.data
import pprint
import pandas as pd
from psychopy import core, event, gui, sound, monitors, parallel
import time
from datetime import datetime
 
#Before starting:
#1) Select output_path (line 21 for TMS lab)
#2) Select if trigger is True or False (line 25)
#output_path = 'C:/Users/hnp_user/Documents/GitHub/ItsAllAboutMotion_stimuli/'

output_path = '/Users/annagaglianese/Desktop/'
offset = False
trigger = False
parallel.setPortAddress(0xDFE8)

# Button box :grbz -> getKeys("g","r","b","z")
# Window features for the Scanner PC(1280x1024)

#clear command prompt

os.system('cls' if os.name == 'nt' else 'clear')

#Providing Subj_ID + Trial
gui = psychopy.gui.Dlg()

gui.addField("Subject ID:")
gui.addField("Trial:")

gui.show()
subj_id = gui.data[0]
trial = str(gui.data[1])

# Stimuli creation

#win = psychopy.visual.Window(
#    units="pix",
#    size=[800,400],
#    fullscr=False
#)
mon = monitors.Monitor('monitor2')
mon.setDistance(57)  # View distance cm
mon.setSizePix([1920, 1080])
mon.setWidth(52.71)  # cm
win = psychopy.visual.Window(fullscr=False, units='pix', screen = 2, winType = 'pyglet', monitor=mon, checkTiming=True)
fps = win.getActualFrameRate()
win.setMouseVisible(False)

##Stimuli
#SF numerical order
AudioDict={}
#for s in listSound:
#        AudioDict[s]=sound.Sound(s)
#print(AudioDict[0])
AudioDict[7]=sound.Sound('../20220331_lePoulpe_auditorySpatialFrequency/rms_length-0p250_freq-3_dir-leftward')
AudioDict[8]=sound.Sound('../20220331_lePoulpe_auditorySpatialFrequency/rms_length-0p250_freq-3_dir-rightward')
AudioDict[9]=sound.Sound('../20220331_lePoulpe_auditorySpatialFrequency/length-0p250_dir-static')

AudioDict[10]=sound.Sound('../20220331_lePoulpe_auditorySpatialFrequency/rms_length-0p250_freq-10_dir-leftward')
AudioDict[11]=sound.Sound('../20220331_lePoulpe_auditorySpatialFrequency/rms_length-0p250_freq-10_dir-rightward')
AudioDict[12]=sound.Sound('../20220331_lePoulpe_auditorySpatialFrequency/length-0p250_dir-static')


outside_grating_1 = psychopy.visual.GratingStim(
    win=win,
    units="pix",
    size=[420,420],
    pos = [0, 0],
    sf = 0.012,
    mask="circle",
    interpolate=True,
    contrast =0.3

)

outside_grating_2 = psychopy.visual.GratingStim(
    win=win,
    units="pix",
    size=[420,420],
    pos = [0, 0],
    sf = 0.038,
    mask="circle",
    interpolate=True,
    contrast =0.3
)

inside_circle = psychopy.visual.Circle(
    win=win,
    units="pix",
    radius = 30,
    fillColor=[0,0,0],
    lineColor=[0,0,0]
)

dot_stim= psychopy.visual.Circle(
    win=win,
    units="pix",
    radius = 5,
)


if offset == True:
    outside_grating_1.pos = [-280,0]
    outside_grating_2.pos = [-280,0]
    inside_circle.pos = [-280,0]
    dots_lr.fieldPos = [-280, 0]
    dots_rl.fieldPos = [-280, 0]
    dots_fix.fieldPos = [-280, 0]
    
#Clocks
clock = psychopy.core.Clock()
total_clock = psychopy.core.Clock()
rt_clock = psychopy.core.Clock()

RT = []

#trails presentation
num_trials_dir = 10
num_trials_fix = 20
trials1 = np.ones(num_trials_dir,dtype=int) * 1;
trials2 = np.ones(num_trials_dir,dtype=int) * 2;
trials3 = np.ones(num_trials_fix,dtype=int) * 3;
trials4 = np.ones(num_trials_dir,dtype=int) * 4;
trials5 = np.ones(num_trials_dir,dtype=int) * 5;
trials6 = np.ones(num_trials_fix,dtype=int) * 6;
trials7 = np.ones(num_trials_dir,dtype=int) * 7;
trials8 = np.ones(num_trials_dir,dtype=int) * 8;
trials9 = np.ones(num_trials_fix,dtype=int) * 9;
trials10 = np.ones(num_trials_fix,dtype=int) * 10;
trials11 = np.ones(num_trials_fix,dtype=int) * 11;
trials12 = np.ones(num_trials_fix,dtype=int) * 12;

tmp_trial = np.array(np.size(trials1)//2*[0] + np.size(trials1)//2*[1])
tmp_trialfix = np.array(np.size(trials3)//2*[0] + np.size(trials3)//2*[1])
np.random.seed(100+np.int(subj_id)+np.int(trial))

np.random.shuffle(tmp_trial)
np.random.shuffle(tmp_trialfix)

trials = np.concatenate((trials1,trials2,trials3,trials4,trials5,trials6,trials7,trials8,trials9,trials10,trials11,trials12))
np.random.shuffle(trials)
TMStrigger = np.array(np.ones(np.size(trials))*100)
trials = np.array(trials)

#print(TMStrigger)
ind_tmp = 0;ind_tmp2 = 0;ind_tmp3 = 0;ind_tmp4 = 0;ind_tmp5 = 0;ind_tmp6 = 0;ind_tmp7 = 0;ind_tmp8 = 0;ind_tmp9 = 0;ind_tmp10 = 0;ind_tmp11 =0;ind_tmp12=0;

for ind,value in enumerate(trials):
    if value==1:
        TMStrigger[ind] = tmp_trial[ind_tmp]
        ind_tmp = ind_tmp+1
    if value==2:
        TMStrigger[ind] = tmp_trial[ind_tmp2]
        ind_tmp2 = ind_tmp2+1   
    if value==3:
        TMStrigger[ind] = tmp_trialfix[ind_tmp3]
        ind_tmp3 = ind_tmp3+1
    if value==4:
        TMStrigger[ind] = tmp_trial[ind_tmp4]
        ind_tmp4 = ind_tmp4+1
    if value==5:
        TMStrigger[ind] = tmp_trial[ind_tmp5]
        ind_tmp5 = ind_tmp5+1
    if value==6:
        TMStrigger[ind] = tmp_trialfix[ind_tmp6]
        ind_tmp6 = ind_tmp6+1
    if value==7:
        TMStrigger[ind] = tmp_trial[ind_tmp7]
        ind_tmp7 = ind_tmp7+1
    if value==8:
        TMStrigger[ind] = tmp_trial[ind_tmp8]
        ind_tmp8 = ind_tmp8+1
    if value==9:
        TMStrigger[ind] = tmp_trialfix[ind_tmp9]
        ind_tmp9 = ind_tmp9+1
    if value==10:
        TMStrigger[ind] = tmp_trialfix[ind_tmp10]
        ind_tmp10 = ind_tmp10+1
    if value==11:
        TMStrigger[ind] = tmp_trialfix[ind_tmp11]
        ind_tmp11 = ind_tmp11+1
    if value==12:
        TMStrigger[ind] = tmp_trialfix[ind_tmp12]
        ind_tmp12 = ind_tmp12+1
#print(trials)
print(TMStrigger)
#trials = np.array([1,2])
# Variables stimulus changes

#intervals = [8,12,9,10,8,11,8,11,12,10,7,8,13,8,12,10,13,7,10,7,13,7,12,13,7,9,8,12]
intervals = np.random.randint(low=3,high=4, size = trials.size)
#intervals = [2,2,2]
stim_duration = 0.1  #durée totale de la stimulation pour chaque block (s)

RT = []
Resp = []
kb = keyboard.Keyboard()
Ratings = []
Time_trials = []
if trigger==False: Time_trigger = np.ones(np.size(trials)) 
else: Time_trigger = []


print(Time_trigger)
##Experiment
clock.reset()
j=1
k=0
y=0
instrTextMov = \
    'Motion - press 1 \n \
    No Motion - press 2  '


instrText = \
'Start '
instrTextRatings = \
    'Left - press Left \n \
    Right - press Right '
instrBreak = 'Take a break. Press b to restart'
tex_Mov = psychopy.visual.TextStim(win=win, text=instrTextMov, font='SimHei')
tex = psychopy.visual.TextStim(win=win, text=instrText, font='SimHei')
tex_Ratings = psychopy.visual.TextStim(win=win, text=instrTextRatings, font='SimHei')
tex_Break = psychopy.visual.TextStim(win=win, text=instrBreak, font='SimHei')
tex.draw()
win.flip()


dot_stim.color ='green'
keys_trigger = psychopy.event.waitKeys(keyList=["t"])#Wait trigger MRI
total_clock.reset()
Date1=datetime.now()
Time_start= str(Date1.time())
#print(Time_start) #time of the experiment
# decompte
tic_start = time.time()
#outside_grating_1.sf=sflist[y]/380
#outside_grating_1.draw()
#inside_circle.draw()
dot_stim.draw()
win.flip()
pulse_started = False
pulse_ended = False
core.wait(3)
for i_trials in trials:
    if trigger:
        parallel.setData(0)  # sets just this pin to be high
        pulse_started = False
        pulse_ended = False
    Time_trial_start = time.time()-tic_start
#    print(Time_trial_start)
    Time_trials.append(Time_trial_start)
    
    keep_going = True
    clock.reset()
    if i_trials < 7: 
        stim_duration = 0.1
        wait_time = 0.03

    elif i_trials > 6: 
        stim_duration = 0.5
        wait_time = 0.1
        
    while clock.getTime() > 0 and clock.getTime() < stim_duration:

        if i_trials == 1:
            outside_grating_1.phase = np.mod(clock.getTime() / - 0.5, 1)
            outside_grating_1.draw()
#            inside_circle.draw()
#            dot_stim.draw()
        
            win.flip()
        elif i_trials == 2:
            outside_grating_1.phase = np.mod(clock.getTime() / + 0.5, 1)
            outside_grating_1.draw()
#            inside_circle.draw()
            dot_stim.draw()
        
            win.flip()                    
        
        elif i_trials == 3:
            outside_grating_1.draw()
#            inside_circle.draw()
            dot_stim.draw()        
            win.flip()              

        elif i_trials == 4:
            outside_grating_2.phase = np.mod(clock.getTime() / - 0.5, 1)
            outside_grating_2.draw()
#            inside_circle.draw()
#            dot_stim.draw()
        
            win.flip()
        elif i_trials == 5:
            outside_grating_2.phase = np.mod(clock.getTime() / + 0.5, 1)
            outside_grating_2.draw()
#            inside_circle.draw()
#            dot_stim.draw()
        
            win.flip()                    
        
        elif i_trials == 6:
            outside_grating_2.draw()
#            inside_circle.draw()
#            dot_stim.draw()        
            win.flip()              
        else:
            AudioDict[i_trials].play()
#            core.wait(0.5)
        keep_going=False
        core.wait(wait_time)
        timeTMS = time.time()-tic_start
#        print(timeTMS)
#            parallel.setData(255)
        if trigger and TMStrigger[y]==1:
            if not pulse_started:
                parallel.setData(255)
                pulse_start_time = clock.getTime()
                pulse_started = True
            
            Time_trigger_startall = time.time()-tic_start 
    

            Time_trigger_start = str(round(Time_trigger_startall,2))
            print(Time_trigger_start[0])
            if pulse_started and not pulse_ended:
                if clock.getTime() - pulse_start_time >= 0.01:
                    parallel.setData(0)
                    pulse_ended = True 
        if i_trials > 6 : core.wait(0.5)
        if clock.getTime() > stim_duration:
            if trigger == True:
                if TMStrigger[y] == 1: Time_trigger.append(Time_trigger_startall)
                elif TMStrigger[y] == 0:            
                    Time_trigger.append(0) 
            tic=time.time()
            tex_Mov.draw()
            win.flip()
            Resp_dir=psychopy.event.waitKeys(keyList=["1","2"])
#            win.flip()
            RTtime = time.time()-tic
            RT.append(RTtime)
            Resp.append(np.array(Resp_dir))
            if int(np.array(Resp_dir)) == 1:
                tex_Ratings.draw()
                win.flip()
                Resp_ratings=psychopy.event.waitKeys(keyList=["left","right"])
#            print(Resp_ratings)
                Ratings.append(np.array(Resp_ratings))
                tex_Mov.draw()
                win.flip()
            else:  Ratings.append(np.array(3))

            if y == 50 or y == 100 :
                
                tex_Break.draw()
                win.flip()
                keys_trigger = psychopy.event.waitKeys(keyList=["b"])#Wait trigger MRI
            dot_stim.draw()
            win.flip()
#            print(Resp)
            isi = intervals[y]
            core.wait(isi)
            y = y+1
            keep_going = False
win.close()

#print(RT) # shows when the participant press a key
#print(Ratings)
#print(Resp)

#Performances
trials_res = trials
trials_res = np.where((trials_res == 1  ), 1, trials_res)
trials_res = np.where((trials_res == 2  ), 2, trials_res)
trials_res = np.where((trials_res == 3  ), 3, trials_res)
trials_res = np.where((trials_res == 4  ), 2, trials_res)
trials_res = np.where((trials_res == 5  ), 1, trials_res)
trials_res = np.where((trials_res == 6  ), 3, trials_res)
trials_res = np.where((trials_res == 7  ), 1, trials_res)
trials_res = np.where((trials_res == 8  ), 2, trials_res)
trials_res = np.where((trials_res == 9  ), 3, trials_res)
#print(trials_res)


Resp = [int(a) for a in Resp]
Ratings = [int(1) if a=='left' else a for a in Ratings]
Ratings = [int(2) if a=='right' else a for a in Ratings]
trials_res = [int(a) for a in trials_res]


per = np.array(Resp) == np.array(trials_res) 

performance = np.count_nonzero(per)
performance = performance/np.size(trials)*100


data = pd.DataFrame ({'Subject':subj_id,
                      'Trial' :trial,
                      'RT': RT,
                      'conditions' : trials,
                      '1 Left 2 Right 3 No Motion': Ratings,
                      'trials_seq': trials_res,
                      'Time_trials': Time_trials,
                      'TMStrigger': TMStrigger,
                      'Time_trigger':Time_trigger,
                      'Motion/No Motion': Resp,

                      })
#print(data)
#Creating data frame
#Name output file path

#output_path = os.path.dirname(os.path.abspath(__file__))
save_name1 = 'subjID' 
save_name2 = subj_id 
save_name3 = '_trial'
save_name4 = trial + '_' + Date1.strftime('%d%m%Y') + 'visualSound_TMS.csv'
save_file = output_path + save_name1 + save_name2 + save_name3 + save_name4
data.to_csv(save_file, index=False, sep = ";")

df1 = data.groupby(['TMStrigger','conditions',]).apply(lambda x : (x['trials_seq'] == x['1 Left 2 Right 3 No Motion']).sum())
df2 = df1.loc[:,[3,6,9]].div(20)*100 #static perfomances 1:sf1_left 2: sf1_right 3: sf1_static 4: dots_right 5:dots_left 6:dots_static 7:sf2_left 8: sf2_right 9: sf2_Static 
print(df2)
df_static = df1.loc[:,[1,2,4,5,7,8]].div(10)*100 #motion perfomances
print(df_static)