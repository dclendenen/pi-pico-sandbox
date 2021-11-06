from machine import Pin, Timer
import time
import micropython
micropython.alloc_emergency_exception_buf(512)

toggle_pin = Pin(3, Pin.OUT)
timer = Timer()

def timer_callback(timer):
    toggle_pin.toggle()

timer.init(freq=2000, mode=Timer.PERIODIC, callback=timer_callback)

try:
    while True:
        time.sleep_us(1)
except:
    print("ended")