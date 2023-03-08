import requests
import re

from departure_time_info import DepartureTimeInfo

URL_TEMPLATE = "http://www.cambridgeshirebus.info/Popup_Content/WebDisplay/WebDisplay.aspx?stopRef="

# Bus Stop IDs
BUSWAY_SHIRE_HALL_N = "0500CCITY497"

# Regexes
# Departure Time Regex
DEPARTURE_TIME_REGEX = 'meItem".+>([\S ]+)<'


def get_departure_html(stop_id: str):
    """!
    Return the departures pop-up HTML for the stop given in stop_id.

    @param stop_id  str The stop ID to query.

    @return The full HTML of the departures pop-up window
    """

    r = requests.get(URL_TEMPLATE + stop_id)

    if r.status_code == 200:
        return str(r.content)

    else:
        raise ValueError(f"URL Returned an invalid response: {r}")


def get_departure_time_strs(departures_html):
    """!
    Extract the strings containing the departure time strs from the departures popup HTML.

    The data contained is not interpreted, it is just a string (e.g. 10 Mins, 10:12, Due).

    @params departures_html The HTML received for the departures pop-up.

    @returns    A list of departure time strs.
                If there are no departures an empty list is returned.
    """
    # Split the HTML into lines
    html_lines = departures_html.split("\\r\\n")

    # Get the lines containing departure times
    departure_lines = [line for line in html_lines if "gridDestinationItem" in line]

    # Strip away the HTML, leaving just a string detailing the departure
    return [re.search(DEPARTURE_TIME_REGEX, line).group(1) for line in departure_lines]


def get_departures_dict(departure_lines):
    """!
    Convert the strings extracted from HTML to useful representations of data.

    @param departure_lines A list of strs representing departures (e.g. "10 Mins"j, "Due")

    @returns A list of DepartureTimeInfo objects generated from departure_lines
    """

    return [DepartureTimeInfo(line) for line in departure_lines]


if __name__ == "__main__":
    html = get_departure_html(BUSWAY_SHIRE_HALL_N)
    lines = get_departure_time_strs(html)
    print(get_departures_dict(lines))

    print(get_departures_dict(["Due", "10 Mins", "18:00"]))
