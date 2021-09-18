from machine import Pin
import time

led_pin = Pin(25, Pin.OUT)
trigger_pin = Pin(17, Pin.OUT)
echo_pin = Pin(19, Pin.IN)

def pulse_gen(pulse_pin, pulse_on_time):
    """Generate a single positive pulse of duration ``pulse_on_time`` on output pin ``pulse_pin`` """
    pulse_pin.high()
    time.sleep_ms(pulse_on_time)
    pulse_pin.low()

def echo_pin_irq():
    print("Echo")


echo_pin.irq(echo_pin_irq, Pin.IRQ_RISING, hard=True)




while True:
    pulse_gen(trigger_pin, 20)
    pulse_gen(led_pin, 1000)
    time.sleep_ms(1000)