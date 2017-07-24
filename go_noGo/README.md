# Go-NoGo task for EEG and fMRI created for  Psychopy 1.83

Simple Go-NoGo tasks with 'O' and 'X' as Go and NoGo stimuli (respectively). 

In the fMRI task, onset times are collected from "times.par" file. Starting trigger is mouse left click.
Press esc to exit.


In the fMRI task tasks are defined in the first lines of the code.
The task looks for a parallel port to send triggers.
It also looks if a cedrus response box is available, if not, responses should
be given in keyboard's space bar.
Relevant data is stored in an excel file inside "data" folder