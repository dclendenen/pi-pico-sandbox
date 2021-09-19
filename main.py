from machine import Pin
import time
import micropython
micropython.alloc_emergency_exception_buf(512)



class DistanceFinder():
    def __init__(self) -> None:
        self.led_pin = Pin(25, Pin.OUT)
        self.trigger_pin = Pin(13, Pin.OUT)
        self.echo_pin = Pin(14, Pin.IN)
        self.rising_edge = False
        self.falling_edge = False
        self.loop_period = 100 # ms
        self.loop_rate = 10 # Hz
        self.sleep_counter = 0
        self.pulse_period_count = int(1/(self.loop_period * self.loop_rate) * 1000)
        self.echo_pulse_start_time = 0
        self.echo_pulse_end_time = 0
        self.new_distance_ready = False

        self.too_close_range = 100 # cm
        self.too_far_range = 200 # cm
        self.just_right_range = 150 #cm

        self.cm_conversion = 58
        self.in_conversion = 148

    def pulse_gen(self, pulse_pin, pulse_on_time):
        """Generate a single positive pulse of duration ``pulse_on_time`` (us) on output pin ``pulse_pin`` """
        pulse_pin.high()
        time.sleep_us(pulse_on_time)
        pulse_pin.low()

    def echo_pin_irq(self, interrupt_source):
        if interrupt_source.value() == 1: # Rising edge
            if self.rising_edge is False:
                self.rising_edge = True
                self.echo_pulse_start_time = time.ticks_us()
        else:
            if self.falling_edge is False:
                self.falling_edge = True
                self.echo_pulse_end_time = time.ticks_us()
        
        if self.rising_edge == True and self.falling_edge == True:
            self.new_distance_ready = True


    def calculate_distance(self, units):
        pulse_width = self.echo_pulse_end_time - self.echo_pulse_start_time
        self.rising_edge = False
        self.falling_edge = False
        if pulse_width < 0:
            pulse_width = 0
            return pulse_width

        if units == 'cm':
            pulse_width = pulse_width / self.cm_conversion
        elif units == 'in':
            pulse_width = pulse_width / self.in_conversion

        return pulse_width

    def setup_irq(self):
        self.echo_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.echo_pin_irq, hard=True)


df = DistanceFinder()
df.setup_irq()

while True:
    if df.sleep_counter < df.pulse_period_count:
        df.sleep_counter += 1
        if df.new_distance_ready is True:
            print(df.calculate_distance('cm'), 'cm')
            df.new_distance_ready = False

        time.sleep_ms(df.loop_period)
    else:
        df.sleep_counter = 0
        df.pulse_gen(df.trigger_pin, 20)