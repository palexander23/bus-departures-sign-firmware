import time

# from api import get_departures, BUSWAY_SHIRE_HALL_N
from api import get_departures, BUSWAY_SHIRE_HALL_N
from departure_time_info import DepartureTimeInfo
from wifi import init_wifi

# Terminal Control Codes
LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"


def init():
    init_wifi()


def main():
    init()

    while 1:
        # Get the departures info
        departures = get_departures(BUSWAY_SHIRE_HALL_N)
        num_departures = len(departures)

        # Print each departure to the dislpay
        for departure in departures:
            print(f"{departure.service:4}{departure.destination:15}{departure.time}")

        time.sleep(1)

        # Bring the cursor back to the top of the departures list
        for n in range(num_departures):
            print(LINE_UP, end=LINE_CLEAR)


if __name__ == "__main__":
    main()
