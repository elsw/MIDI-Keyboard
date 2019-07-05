#/bin/sh

pigpiod
python3 keyboard_write_only.py &
python3 keyboard_read_only.py &