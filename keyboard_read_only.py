import mido
import pigpio
import time
import board
import neopixel

LOOP_TIME = 0.04 #40ms


TOTAL_KEYS = 61
KEYS_ROWS = 8
KEYS_COLUMNS = 8

LED_MAX = 150
MIDI_MIN = 36
MIDI_MAX = 100

#note = 1, sharp = 0
LED_COLOUR = [(255,255,0),(255,0,0)]
LED_OCTAVE = [0,1,0,1,1,0,1,0,1,0,1,1]
LED_OCTAVE_START = [1,25,49,73,97]
LED_FLIP = True
LED_TOTAL = 5 * 24
LED_ECHO = False


input_port = mido.open_input('f_midi') # open USB port
pixels = neopixel.NeoPixel(board.D18, LED_MAX,auto_write=False)
pixels.fill((0, 0, 0))


loop_counter = 0
loop_counts = 10
loop_time = [0.0] * loop_counts

while True:
    start_time = time.time()

    for msg in input_port.iter_pending():
        if(msg.type == 'note_on' or msg.type == 'note_off'):
            octave = int((msg.note - MIDI_MIN - 1) / 12)
            note = (msg.note - MIDI_MIN - 1) % 12
                                
            led_pixel = LED_OCTAVE_START[octave] + (note * 2)
            if(LED_FLIP):
                led_pixel = LED_TOTAL - led_pixel - 1
                    
            if(msg.type == 'note_on'):
                pixels[led_pixel] = LED_COLOUR[LED_OCTAVE[note]]
                pixels[led_pixel + 1] = LED_COLOUR[LED_OCTAVE[note]]
            else:
                pixels[led_pixel] = (0,0,0)
                pixels[led_pixel + 1] = (0,0,0)
    pixels.show()
    
    end_time = time.time()
    time_taken = (end_time - start_time)
    if(time_taken < LOOP_TIME):
        time.sleep(LOOP_TIME - time_taken)

    #end_time = time.time()
    #time_taken = (end_time - start_time)    
    #loop_time[loop_counter] = time_taken
    #loop_counter = loop_counter + 1
    #if(loop_counter >= loop_counts):
    #    loop_counter = 0
    #    print("Loop average",sum(loop_time) / len(loop_time))
            
