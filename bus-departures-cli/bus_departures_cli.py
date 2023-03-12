import time

from api import get_departures, BUSWAY_SHIRE_HALL_N

# Terminal Control Codes
LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"


def main():
    print("==================")
    print("Bus Departures CLI")
    print("==================")
    print("")

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
