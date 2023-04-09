import time

from api import get_departures
from departure_time_info import DepartureTimeInfo
from wifi import init_wifi
from config import STOP_ID
from led import led_init
from wdt import wdt_init, wdt_wait_ms, wdt_feed

# Automatically import the correct display interface
# EPD when running micropython, terminal otherwise
try:
    import machine

    from display_epd import display_init, display_update
except:
    from display_hosted import display_init, display_update

# Terminal Control Codes
LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"

# Timing Constants
DISPLAY_REFRESH_RATE_ms = 10000


def init():
    led_init()
    init_wifi()
    display_init()
    wdt_init(8000)

    print("Bus Departures v1.0.0")


def main():
    init()

    prev_num_departures = 0

    counter = 0

    while 1:
        # Get the departures info
        departures_list = get_departures(STOP_ID)
        wdt_feed()

        # Update the display
        # EPD if running on embedded, terminal if running hosted
        display_update(departures_list)
        wdt_feed()

        # Delay so it's not constantly updating
        wdt_wait_ms(DISPLAY_REFRESH_RATE_ms, 1000)


if __name__ == "__main__":
    main()
