try:
    from machine import WDT

    HOSTED = False
except:
    HOSTED = True

watchdog = None

import time


def wdt_init(wdt_timeout_ms):
    if HOSTED:
        return

    global watchdog

    watchdog = WDT(timeout=wdt_timeout_ms)


def wdt_feed():
    if HOSTED:
        return

    global watchdog

    watchdog.feed()


def wdt_wait_ms(delay_ms, wdt_interval_ms):
    """Blocking wait for ms given in delay_ms.
    Taken in blocks of wdt_interval_ms, resetting the watchdog after each chunk.
    """

    if HOSTED:
        time.sleep(delay_ms / 1000)
        return

    while delay_ms > wdt_interval_ms:
        time.sleep_ms(wdt_interval_ms)
        delay_ms -= wdt_interval_ms
        wdt_feed()

    if delay_ms > 0:
        time.sleep_ms(delay_ms)
        wdt_feed()
