from machine import Pin
import time

led_pin = Pin(25, Pin.OUT)
trigger_pin = Pin(13, Pin.OUT)
echo_pin = Pin(15, Pin.IN)

def pulse_gen(pulse_pin, pulse_on_time):
    """Generate a single positive pulse of duration ``pulse_on_time`` (us) on output pin ``pulse_pin`` """
    pulse_pin.high()
    time.sleep_us(pulse_on_time)
    pulse_pin.low()

def echo_pin_irq():
    led_pin.toggle()


echo_pin.irq(echo_pin_irq, Pin.IRQ_RISING, hard=False)




while True:
    pulse_gen(trigger_pin, 20)
    time.sleep_ms(1000)