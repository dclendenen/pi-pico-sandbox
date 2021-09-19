from machine import Pin
import time
import micropython
micropython.alloc_emergency_exception_buf(512)



class DistanceFinder():
    def __init__(self) -> None:
        self.board_led = Pin(25, Pin.OUT)
        self.trigger_pin = Pin(13, Pin.OUT)
        self.echo_pin = Pin(14, Pin.IN)
        self.too_far_led = Pin(0, Pin.OUT)
        self.goldilocks_led = Pin(1, Pin.OUT)
        self.too_close_led = Pin(2, Pin.OUT)

        self.all_system_leds = [self.board_led, self.too_close_led, self.too_far_led, self.goldilocks_led]

        self.rising_edge = False
        self.falling_edge = False
        self.loop_period = 100 # ms
        self.loop_rate = 10 # Hz
        self.sleep_counter = 0
        self.pulse_period_count = int(1/(self.loop_period * self.loop_rate) * 1000)
        self.echo_pulse_start_time = 0
        self.echo_pulse_end_time = 0
        self.new_distance_ready = False
        self.system_functional = False

        self.too_close_threshold = 80 # cm
        self.too_far_threshold = 200 # cm
        self.just_right_threshold = 110 #cm

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

    def bearify_distance(self, measured_distance):
        if measured_distance >= self.too_far_threshold:
            pass
        elif measured_distance <= self.too_close_threshold:
            pass
        elif measured_distance <= self.just_right_threshold:
            pass

    def setup_irq(self):
        self.echo_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.echo_pin_irq, hard=True)

    def reset_leds(self):
        self.too_close_led.high()
        self.too_far_led.high()
        self.goldilocks_led.high()

    def toggle_leds(self, leds, rate, blinks):
        period = int(1 / rate * 1000) # ms

        self.reset_leds()

        for blink in range(blinks):
            for led in leds:
                led.toggle()
            time.sleep_ms(period)

            for led in leds:
                led.toggle()
            time.sleep_ms(period)

            
    def post(self):
        self.too_close_led.high()
        self.too_far_led.high()
        self.goldilocks_led.high()

        time.sleep(1)

        self.pulse_gen(self.trigger_pin, 20)

        time.sleep(1)

        if self.new_distance_ready is True:
            self.toggle_leds(self.all_system_leds, 10, 10)
            self.system_functional = True




df = DistanceFinder()
df.setup_irq()
df.post()

while True:
    if df.system_functional is True:
        if df.sleep_counter < df.pulse_period_count:
            df.sleep_counter += 1
            if df.new_distance_ready is True:
                print(df.calculate_distance('cm'), 'cm')
                df.new_distance_ready = False

            time.sleep_ms(df.loop_period)
        else:
            df.sleep_counter = 0
            df.pulse_gen(df.trigger_pin, 20)
    else:
        print("System error. System non-functioning.")
        df.toggle_leds(df.all_system_leds, 5, 5)
        df.post()