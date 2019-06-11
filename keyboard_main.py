import mido
import pigpio

TOTAL_KEYS = 61
KEYS_ROWS = 8
KEYS_COLUMNS = 8

GPIO_ROWS = [24,10,9,25,11,8,7,5] # Outputs
GPIO_COLUMNS = [6,12,13,19,16,26,20,21] #Inputs

KEY_TO_MIDI_NOTE = [\
    list(range(27,35)),\
    list(range(35,43)),\
    list(range(43,51)),\
    list(range(51,58)),\
    list(range(58,65)),\
    list(range(65,73)),\
    list(range(73,81)),\
    list(range(81,89)) ]

KEY_STATES = [ [1] * KEYS_COLUMNS ] * KEYS_ROWS

# 0 (low) = ON , 1 (high) = OFF
KEY_STATE = ['note_on','note_off']

pi = pigpio.pi()
output = mido.open_output('f_midi')

#setup GPIO
for LED in GPIO_COLUMNS:
    print("Setup input GPIO " + str(LED))
    pi.set_mode(LED, pigpio.INPUT)
    pi.set_pull_up_down(LED, pigpio.PUD_UP)

for LED in GPIO_ROWS:
    print("Setup output GPIO " + str(LED_)
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
                print("Key " + str(KEY_TO_MIDI_NOTE[i][j]) + " " + KEY_STATE[state])
                
    pi.write(GPIO_ROWS[KEYS_ROWS-1],1)
            
