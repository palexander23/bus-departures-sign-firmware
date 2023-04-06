import time

# from api import get_departures, BUSWAY_SHIRE_HALL_N
from api import get_departures
from departure_time_info import DepartureTimeInfo
from wifi import init_wifi
from config import STOP_ID

# Terminal Control Codes
LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"


def init():
    init_wifi()


def main():
    init()

    prev_num_departures = 0

    while 1:
        # Get the departures info
        departures = get_departures(STOP_ID)
        num_departures = len(departures)

        # Print each departure to the dislpay
        for departure in departures:
            print(
                f"{departure.service:4}{departure.destination:20}{departure.time:>10}"
            )

        # Clear the rest of the screen that was not overwritten with this print
        if prev_num_departures > num_departures:
            for n in range(prev_num_departures - num_departures):
                print(LINE_UP, end=LINE_CLEAR)

        time.sleep(1)

        # Bring the cursor back to the top of the departures list
        for n in range(num_departures):
            print(LINE_UP, end="")


if __name__ == "__main__":
    main()
