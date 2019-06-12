import mido
import pigpio
import time

TOTAL_KEYS = 61
KEYS_ROWS = 8
KEYS_COLUMNS = 8

GPIO_COLUMNS = [24,10,9,25,11,8,7,5] # Outputs
GPIO_ROWS = [6,12,13,19,16,26,20,21] #Inputs

KEY_TO_MIDI_NOTE = [\
    list(range(36,44)),\
    list(range(44,52)),\
    list(range(52,60)),\
    list(range(60,68)),\
    list(range(68,76)),\
    list(range(76,84)),\
    list(range(84,92)),\
    list(range(92,100)) ]

KEY_STATES = dict()
#fill dictinoary with states for each midi note
for i in range(0, KEYS_ROWS):
    for j in range(0, KEYS_COLUMNS):
        KEY_STATES[KEY_TO_MIDI_NOTE[j][i]] = 1

# 0 (low) = ON , 1 (high) = OFF
KEY_VALUE = ['note_on','note_off']

pi = pigpio.pi()
output = mido.open_output('f_midi')

loop_counter = 0
loop_counts = 10
loop_time = [0.0] * loop_counts

#setup GPIO
for i in GPIO_COLUMNS:
    print("Setup input GPIO ",i)
    pi.set_mode(i, pigpio.INPUT)
    pi.set_pull_up_down(i, pigpio.PUD_UP)

for i in GPIO_ROWS:
    print("Setup output GPIO ",i)
    pi.set_mode(i, pigpio.OUTPUT)

while True:
    #start_time = time.time()
    for i in range(0 , KEYS_ROWS):
        #set i row low
        if i > 0:
            pi.write(GPIO_ROWS[i-1],1)
        pi.write(GPIO_ROWS[i],0)
        gpio_state = pi.read_bank_1()
        #if i == 0:
            #print(bin(gpio_state))
        for j in range(0 , KEYS_COLUMNS):
            #read column
            state = (gpio_state & (1 << GPIO_COLUMNS[j])) > 0
            midi_note = KEY_TO_MIDI_NOTE[j][i]
            if KEY_STATES[midi_note] != state:
                output.send(mido.Message(KEY_VALUE[state], note = midi_note , velocity = 127))
                KEY_STATES[midi_note] = state
                #print("Key ",midi_note,KEY_VALUE[state])
                
    pi.write(GPIO_ROWS[KEYS_ROWS-1],1)
    #end_time = time.time()
    #loop_time[loop_counter] = (end_time - start_time)
    #loop_counter = loop_counter + 1
    #if(loop_counter >= loop_counts):
        #loop_counter = 0
        #print("Loop average",sum(loop_time) / len(loop_time))
            
