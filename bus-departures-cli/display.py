try:
    import machine
    import gc

    from micropython_nano_gui.drivers.ePaper2in9 import EPD as SSD
    from micropython_nano_gui.core.nanogui import refresh

    HOSTED = False
except:
    HOSTED = True

from time import sleep


from departure_time_info import DepartureTimeInfo

ssd = None

RST_PIN = 12
DC_PIN = 8
CS_PIN = 9
BUSY_PIN = 13


def display_init():
    # Don't run any micropython stuff if we're running embedded
    if HOSTED:
        return

    # Initialize a display controller
    # Copied from file color_setup.py in Waveshare example code
    prst = machine.Pin(RST_PIN, machine.Pin.OUT)
    pbusy = machine.Pin(BUSY_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
    pcs = machine.Pin(CS_PIN, machine.Pin.OUT)
    spi = machine.SPI(1, baudrate=4_000_000)
    pdc = machine.Pin(DC_PIN, machine.Pin.OUT)
    gc.collect()  # Precaution before instantiating framebuf

    global ssd
    ssd = SSD(spi, pcs, pdc, prst, pbusy, landscape=True, asyn=False)

    display_clear(ssd)
    ssd.wait_until_ready()


def display_update(departure_list: list[DepartureTimeInfo]):
    if HOSTED:
        return


def display_clear(ssd):
    refresh(ssd, True)
