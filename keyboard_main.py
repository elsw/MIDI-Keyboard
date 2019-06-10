import mido
import pigpio

TOTAL_KEYS = 61
KEYS_ROWS = 8
KEYS_COLUMNS = 8

GPIO_ROWS = [1,2,3,4,5,6,7,8]
GPIO_COLUMNS = [9,10,11,12,13,14,15,16]

KEY_TO_MIDI_NOTE = [\
    [21,22,23,24,25,26,27,28],\
    [21,22,23,24,25,26,27,28],\
    [21,22,23,24,25,26,27,28],\
    [21,22,23,24,25,26,27,28],\
    [21,22,23,24,25,26,27,28],\
    [21,22,23,24,25,26,27,28],\
    [21,22,23,24,25,26,27,28],\
    [21,22,23,24,25,26,27,28] ]

KEY_STATES = [ [1] * KEYS_COLUMNS ] * KEYS_ROWS

# 0 (low) = ON , 1 (high) = OFF
KEY_STATE = ['note_on','note_off']

pi = pigpio.pi()
output = mido.open_output('f_midi')

#setup GPIO
for LED in GPIO_COLUMNS:
   pi.set_mode(LED, pigpio.INPUT)
   pi.set_pull_up_down(LED, pigpio.PUD_UP)

for LED in GPIO_ROWS:
   pi.set_mode(LED, pigpio.OUTPUT)

while True:
    for i in range(0 , KEYS_ROWS):
        #set i row low
        if i > 0:
            pi.write(GPIO_ROWS[i-1],1)
        pi.write(GPIO_ROWS[i],0)
        for j in range(0 , KEYS_COLUMNS):
            #read column
            state = pi.read(GPIO_COLUMNS[j])
            if state != KEY_STATES[i][j]:
                output.send(mido.Message(KEY_STATE[state], note = KEY_TO_MIDI_NOTE[i][j] , velocity = 127))
                KEY_STATES[i][j] = state
                
    pi.write(GPIO_ROWS[KEYS_ROWS-1],1)
            
