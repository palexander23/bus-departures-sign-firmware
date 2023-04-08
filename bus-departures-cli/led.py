try:
    from machine import Pin, Timer

    HOSTED = False
except:
    HOSTED = True

import time

led = None
flash_timer = None


def led_init():
    if HOSTED:
        return

    print("LED INIT")
    global led
    led = Pin("LED", Pin.OUT)

    led_on()
    time.sleep_ms(50)
    led_off()
    time.sleep_ms(200)

    led_on()
    time.sleep_ms(50)
    led_off()
    time.sleep_ms(200)

    global flash_timer


def led_start_flash_pattern(flash_len_ms, flash_gap_ms):
    global flash_timer
    flash_timer = Timer(
        period=flash_len_ms * 1000,
        mode=Timer.ONE_SHOT,
        callback=lambda t: led_flash(flash_len_ms),
    )


def led_flash(flash_len_ms):
    if HOSTED:
        return

    global led
    led_on()
    time.sleep_ms(50)
    led_off()


def led_on():
    if HOSTED:
        return

    global led
    led.on()


def led_off():
    if HOSTED:
        return

    global led
    led.off()


def led_toggle():
    if HOSTED:
        return

    global led
    led.toggle()
