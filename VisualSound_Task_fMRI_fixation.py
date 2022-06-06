#Anna Gaglianese February 2022
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
from datetime import datetime
import time
from psychopy import core, event, gui, sound, monitors, parallel

# Button box :grbz -> getKeys("g","r","b","z")
# Window features for the Scanner PC(1280x1024)
output_path = 'C:/Users/lifmet_fmri_A/Documents/MATLAB/Anna/GitHub/ItsAllAboutMotion_stimuli/'
#output_path = '/Users/annagaglianese/Desktop/'

#clear command prompt

os.system('cls' if os.name == 'nt' else 'clear')

#Providing Subj_ID + Trial
gui = psychopy.gui.Dlg()

gui.addField("Subject ID:")
gui.addField("Trial:")

gui.show()
subj_id = gui.data[0]
trial = str(gui.data[1])

# Stimuli creation3
mon = monitors.Monitor('test')

win = psychopy.visual.Window(
    units="pix",
    size=[1440,900],
#    monitor=mon, 
    checkTiming=True,
    screen = 1,
    winType = 'pyglet',
    fullscr=False
)

#Stimuli
outside_grating_1 = psychopy.visual.GratingStim(
    win=win,
    units="pix",
    size=[380,380],
    sf= 0.003, #0.011, # #5.0/962.0, 
    mask="circle",
    interpolate=True
)

outside_grating_2 = psychopy.visual.GratingStim(
    win=win,
    units="pix",
    size=[380,380],
    sf= 0.003, #0.011, # 0.003, #5.0/962.0, 0.011,
    mask="circle",
    interpolate=True
)

outside_grating_3 = psychopy.visual.GratingStim(
    win=win,
    units="pix",
    size=[380,380],
    sf = 0.011,
    mask="circle",
    interpolate=True
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

dots_lr = psychopy.visual.DotStim(win=win, color = 'Black',speed = 1, dotLife = 100,fieldShape = 'circle', dir = 0, fieldSize = [380,380], dotSize = 8, coherence = 1, noiseDots=('direction'),nDots = 100)
dots_rl = psychopy.visual.DotStim(win=win, color = 'Black',speed = 1, dotLife = 100,fieldShape = 'circle', dir = 180, fieldSize = [380,380], dotSize = 8, coherence = 1, noiseDots=('direction'),nDots = 100)

listSound=[]
AudioDict={}
AudioDict[4]=sound.Sound('../audio_fMRI/rms-length-1p-freq-3-dir-biward')
AudioDict[5]=sound.Sound('../audio_fMRI/rms-length-1p-freq-10-dir-biward')
AudioDict[6]=sound.Sound('../audio_fMRI/rms-length-1p-freq-fullmotion-dir-biward')
#AudioDict[4]=sound.Sound('../20220331_lePoulpe_auditorySpatialFrequency/rms_length-0p5-freq-3_dir-leftward')
#AudioDict[5]=sound.Sound('../20220331_lePoulpe_auditorySpatialFrequency/rms_length-0p5-freq-10_dir-rightward')
#AudioDict[6]=sound.Sound('../20220331_lePoulpe_auditorySpatialFrequency/length-1.2_dir-static.wav')


#Clocks
clock = psychopy.core.Clock()
total_clock = psychopy.core.Clock()
rt_clock = psychopy.core.Clock()

#Variables color changes
color_start = 1;# np.random.randint(0,2)
randomlist_start = []
randomlist_end = []
for i in range(0,40):
    n = random.randint(2,308)
    m = n + 0.5
    randomlist_start.append(n)
    randomlist_end.append(m)
    
randomlist_start = [3, 7, 13, 16, 33, 36, 53, 54, 58, 62, 66, 70, 90, 92, 96, 106, 110, 125, 128, 135, 140, 142, 162, 166, 172, 178, 190, 194, 202, 216, 220, 236, 240, 248, 258, 273, 278, 292, 300, 308, 318, 324 ]
randomlist_end = [3.5, 7.5, 13.5, 16.5, 33.5, 36.5, 53.5, 54.5, 58.5, 62.5, 66.5, 70.5, 90.5, 92.5, 96.5, 106.5, 110.5, 125.5, 128.5, 135.5, 140.5, 142.5, 162.5, 166.5, 172.5, 178.5, 190.5, 194.5, 202.5, 216.5, 220.5, 236.5, 240.5, 248.5, 258.5, 273.5, 278.5, 292.5, 300.5, 308.5, 318.5, 324.5 ]

time_dot_color_start = (randomlist_start)
time_dot_color_end = (randomlist_end)


# Variables stimulus changes
#trails presentation
num_trials_dir = 3
#num_trials_fix = 10
trials1 = np.ones(num_trials_dir,dtype=int) * 1;
trials2 = np.ones(num_trials_dir,dtype=int) * 2;
trials3 = np.ones(num_trials_dir,dtype=int) * 3;
trials4 = np.ones(num_trials_dir,dtype=int) * 4;
trials5 = np.ones(num_trials_dir,dtype=int) * 5;
trials6 = np.ones(num_trials_dir,dtype=int) * 6;
trials = np.concatenate((trials1,trials2,trials3,trials4,trials5,trials6))
np.random.seed(100+np.int(trial))
np.random.shuffle(trials)
# Variables stimulus changes
trials = [1, 4, 6, 2, 5, 3, 6, 3, 4, 1, 2, 5, 6, 3, 5, 4, 2, 1]
print(trials)

stim_start = 1 # rajouter 8 secondes de pause juste après qu'on lance le scanner (pas oublier waitKeys()) - grating immobile (s) -> waitKeys() "t" for scanner
stim_1_duration = 0.5 # grating bouge à gauche (s)
stim_2_duration = 0.5 # grating bouge à droite (s)
stim_duration = stim_1_duration + stim_2_duration #durée totale de la stimulation pour chaque block (s)
total_time = 312+stim_start # temps total de la tâche (s)
Time_trials = []

RT = []

kb = keyboard.Keyboard()

##Experiment
clock.reset()
j=1
k=0
tex_Start = psychopy.visual.TextStim(win=win, text='Waiting for trigger', font='SimHei')

if color_start == 1:
    dot_stim.color ='green'
#    outside_grating_1.draw()

    tex_Start.draw()
    win.flip()

    keys_trigger = psychopy.event.waitKeys(keyList=["6"])#Wait trigger MRI
    dot_stim.draw()
    win.flip()

    Date1=datetime.now()
    Time_start= str(Date1.time())
    Tic_start =  time.time()
    print(Time_start) #time of the experiment
    total_clock.reset()
    core.wait(stim_start)
    for idx, i_trials in enumerate(trials):
        keep_going = True
        clock.reset()
        Time_trial_start = time.time()-Tic_start
        Time_trials.append(Time_trial_start)    
        for i in range(0,10):
            clock.reset()
            if i_trials < 4:
                while clock.getTime() > 0 and clock.getTime() < stim_1_duration:
                    if total_clock.getTime() > time_dot_color_end[k]:
                        k = k+1
                    if k>19:
                        k=19
                        
                    if total_clock.getTime() >= time_dot_color_start[k] and total_clock.getTime() < time_dot_color_end[k]:
                        dot_stim.color = 'red'
                    else:
                        dot_stim.color = "green"
                    if i_trials ==1:
                        outside_grating_2.phase = np.mod(clock.getTime() / - 0.5, 1)
                        outside_grating_2.draw()
                        inside_circle.draw()
                        dot_stim.draw()
                        win.flip()
                    elif i_trials==2:
                        outside_grating_3.phase = np.mod(clock.getTime() / - 0.5, 1)
                        outside_grating_3.draw()
                        inside_circle.draw()
                        dot_stim.draw()
                        win.flip()
                    elif i_trials ==3:
                        dots_lr.draw()
                        inside_circle.draw()
                        dot_stim.draw()
                        win.flip()

                      
                    keys = kb.getKeys()
                    for thisKey in keys:
                        if  thisKey == "g" or thisKey =="y" or thisKey =="b" or thisKey == "r":
                            RT.append([thisKey.rt])
                            print(thisKey.name)
                        else: 
                            keep_going = False
                            
    #                if clock.getTime() > stim_1_duration:
    #                    keep_going=False
    #        
                while clock.getTime() > stim_1_duration and clock.getTime() < stim_duration:
                    if total_clock.getTime() > time_dot_color_end[k]:
                        k = k+1
                    if k>19:
                        k=19
                        
                    if total_clock.getTime() >= time_dot_color_start[k] and total_clock.getTime() < time_dot_color_end[k]:
                        dot_stim.color = 'red'
                    else:
                        dot_stim.color = "green"
        
                    if i_trials ==1:
                        outside_grating_2.phase = np.mod(clock.getTime() / + 0.5, 1)
                        outside_grating_2.draw()
                        inside_circle.draw()
                        dot_stim.draw()
                        win.flip()
                    elif i_trials==2:
                        outside_grating_3.phase = np.mod(clock.getTime() / + 0.5, 1)
                        outside_grating_3.draw()
                        inside_circle.draw()
                        dot_stim.draw()
                        win.flip()
                    elif i_trials ==3:
                        dots_rl.draw()
                        inside_circle.draw()
                        dot_stim.draw()
                        win.flip()
        
                    core.wait(0.1)    
                    keys = kb.getKeys()
                    for thisKey in keys:
                        if  thisKey == "3" or thisKey =="2" or thisKey =="1" or thisKey == "4":
                            RT.append([thisKey.rt])
                            print(thisKey.name)
                        else: 
                            keep_going = False
            else:
                AudioDict[i_trials].play()
                core.wait(1.1)
        while clock.getTime() < 8:
            if total_clock.getTime() > time_dot_color_end[k]:
                k = k+1
            if k>19:
                k=19
            
            if total_clock.getTime() >= time_dot_color_start[k] and total_clock.getTime() < time_dot_color_end[k]:
                dot_stim.color = 'red'
            else:
                dot_stim.color = "green"
                 
            inside_circle.draw()
            dot_stim.draw()
            win.flip()
    #core.wait(8)    
            keys = kb.getKeys()
            for thisKey in keys:
                if  thisKey == "3" or thisKey =="2" or thisKey =="1" or thisKey == "4" :
                    RT.append([thisKey.rt])
                    print(thisKey.name)
                else: 
                    keep_going = False
                    
#        if clock.getTime() > stim_duration + 2:
#            keep_going = False
                    
    win.close()
Date2=datetime.now()
Time_end= str(Date2.time())
print(Time_end) #time of the experiment
print(time_dot_color_start) #shows time of color change (in seconds)
print(RT) # shows when the participant press a key
accuracy = (len(RT)/len(time_dot_color_start)) *100 
print(accuracy) # shows the accuracy of the participant (in %)

data = pd.DataFrame ({'Subject': subj_id,
                      'Trial' : trial,
                      'Accuracy (%)': accuracy,
                      'Start' : Time_start,
                      'End' : Time_end,
                      'Trials' : trials,
                      'Time' : Time_trials
                      })
print(data)
#Creating data frame
#Name output file path

#output_path = os.path.dirname(os.path.abspath(__file__))
save_name1 = 'subjID' 
save_name2 = subj_id 
save_name3 = '_trial'
save_name4 = trial + '_' + Date1.strftime('%d%m%Y') + ' VisualSound_fMRI_run' + trial + '.csv'
save_file = output_path + save_name1 + save_name2 + save_name3 + save_name4
data.to_csv(save_file, index=False, sep = ";")

