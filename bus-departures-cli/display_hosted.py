import time

from departure_time_info import DepartureTimeInfo

# Terminal Control Codes
LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"


def display_init():
    pass


prev_num_departures = 0


def display_update(departures_list: list[DepartureTimeInfo]):
    global prev_num_departures

    num_departures = len(departures_list)

    # Print each departure to the dislpay
    for departure in departures_list:
        print(f"{departure.service:4}{departure.destination:20}{departure.time:>10}")

    # Clear the rest of the screen that was not overwritten with this print
    if prev_num_departures > num_departures:
        for n in range(prev_num_departures - num_departures):
            print(LINE_UP, end=LINE_CLEAR)

    # Bring the cursor back to the top of the departures list
    for n in range(num_departures):
        print(LINE_UP, end="")

    prev_num_departures = num_departures


def display_clear(ssd):
    pass
