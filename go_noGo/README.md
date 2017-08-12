# Go-NoGo task for EEG and fMRI created for  Psychopy 1.83

Two simple Go-NoGo tasks with 'O' and 'X' as Go and NoGo stimuli, respectively. Includes a version that sends triggers by parallel port to be used in EEG, and fMRI version that waits for the scanner trigger to start.

In the fMRI version, onset times are collected from "times.par" file. Starting trigger is mouse left click.
Press esc to exit.


In the EEG version the task looks for a parallel port to send triggers.
It also looks if a cedrus response box is available, if not, responses should
be given in the keyboard's space bar.

Relevant data is stored in an excel file inside "data" folder