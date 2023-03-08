class DepartureTimeInfo:
    """!
    A class representing the departure of a single bus.

    The Class has 3 ways of representing an departure:
    1) Live Updated Mins to departure as an Integer.
    2) Text representing other information (e.g. "10 Mins", "Cancelled").

    The constructor of the class is fed the item 3, the text representation.
    It will attempt to derive the other two.
    It will leave them as None if it fails.
    """

    def __init__(self, _departure_text):
        self.departure_text = _departure_text
        """Text taken from the HTML representing the departure info."""

        self.departure_mins_int = self._get_mins_integer(self.departure_text)
        """Int encoding the minutes to departure. None if not live departure info."""

    def _get_mins_integer(self, departure_text) -> int:
        """!
        Attempt to derive the integer value for the minutes until the departure.
        If the text is not in the format e.g. "10 Mins" the function will return None.

        @param departure_text The text to attempt to convert.

        @returns Integer encoding number of minutes to departure or None if not convertible.
        """

        # If the text is not a representation of minutes, return None
        if departure_text[-4:] != "Mins":
            return None

        # Remove the mins value from the string
        mins_str = departure_text[:-5]

        # Convert the numerical string to an integer.
        # Return None on a failure.
        try:
            return int(mins_str)
        except Exception as e:
            return None

    def __repr__(self) -> str:
        return f'DepartureTimeInfo({self.departure_mins_int},"{self.departure_text}")'

    def __str__(self) -> str:
        return f'Live Mins: {self.departure_mins_int}\tText: "{self.departure_text}"'
