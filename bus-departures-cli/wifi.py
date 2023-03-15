try:
    import network

    EMBEDDED_HOST = True
except:
    EMBEDDED_HOST = False

from time import sleep

from wifi_credentials import SSID, PSK

CONNECTION_TIMEOUT_LIMIT = 30

# Terminal Control Codes
LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"


def init_wifi():
    # Return immediately if we're not running on a micropython host
    if not EMBEDDED_HOST:
        return

    # Create the station object
    # In this case 'station' means a device that connects to a router
    sta_if = network.WLAN(network.STA_IF)

    # Activate the WiFi Station Interface and enter network details
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(SSID, PSK)

        print("Waiting for connection...")

        timeout = 0
        while not sta_if.isconnected():
            pass

        print(LINE_UP, end=LINE_CLEAR)
