from machine import Pin, PWM
import time
import micropython
micropython.alloc_emergency_exception_buf(512)


pwm_gen = PWM(Pin(3))

pwm_gen.freq(500000)

pwm_gen.duty_u16(32768)

try:
    while True:
        time.sleep_us(1)
except:
    print("ended")