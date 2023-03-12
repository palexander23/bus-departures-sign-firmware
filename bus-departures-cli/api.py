import requests
import re

from departure_time_info import DepartureTimeInfo

URL_TEMPLATE = "http://www.cambridgeshirebus.info/Popup_Content/WebDisplay/WebDisplay.aspx?stopRef="

# Bus Stop IDs
BUSWAY_SHIRE_HALL_N = "0500CCITY497"

# Regexes
DEP_TIME_REGEX = 'meItem"[^<]+>([\S ]+)<'
DEP_SERVICE_REGEX = 'ceItem"[^<]+>([^<]+)<'
DEP_DESTINATION_REGEX = 'ionItem" [^>]+><[^>]+>([^<]+)<'


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


def get_departure_objs(departures_html):
    # Split the HTML into lines
    html_lines = departures_html.split("\\r\\n")

    # Get the lines containing departure times
    lines = [line for line in html_lines if "gridDestinationItem" in line]

    # Extract the departure times, service names, and destinations for each departure in the html
    times = [re.search(DEP_TIME_REGEX, line).group(1) for line in lines]
    services = [re.search(DEP_SERVICE_REGEX, line).group(1) for line in lines]
    destinations = [re.search(DEP_DESTINATION_REGEX, line).group(1) for line in lines]

    return [
        DepartureTimeInfo(time, service, destination)
        for time, service, destination in zip(times, services, destinations)
    ]


def get_departures(stop_id: str) -> list[DepartureTimeInfo]:
    departures_html = get_departure_html(stop_id)
    return get_departure_objs(departures_html)


if __name__ == "__main__":
    import pprint as pp

    html = get_departure_html(BUSWAY_SHIRE_HALL_N)
    pp.pprint(get_departure_objs(html))
