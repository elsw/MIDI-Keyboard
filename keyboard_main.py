import fmidi
import pigpio

TOTAL_KEYS = 61
KEYS_ROWS = 8
KEYS_COLUMNS = 8

GPIO_PINS[KEYS_ROWS+KEYS_COLUMNS] =\
    {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16}

KEY_TO_MIDI_NOTE[KEYS_ROWS][KEYS_COLUMNS] = {\
    {21,22,23,24,25,26,27,28},\
    {21,22,23,24,25,26,27,28},\
    {21,22,23,24,25,26,27,28},\
    {21,22,23,24,25,26,27,28},\
    {21,22,23,24,25,26,27,28},\
    {21,22,23,24,25,26,27,28},\
    {21,22,23,24,25,26,27,28},\
    {21,22,23,24,25,26,27,28} }

KEY_STATES[KEYS_ROWS][KEYS_COLUMNS] = zeros(8,8)

# 0 (low) = ON , 1 (high) = OFF
KEY_STATE = {'note_on','note_off'}

pi = pigpio.

while True:
    for i in range(0 , KEYS_ROWS):
        #output low on i
        for j in range(0 , KEYS_COLUMNS):
            #read column
            bool state = pi.read(GPIO_PINS[KEYS_ROWS+j])
            
