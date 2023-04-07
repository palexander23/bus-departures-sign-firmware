try:
    import machine
    import gc

    from micropython_nano_gui.drivers.ePaper2in9 import EPD as SSD
    from micropython_nano_gui.core.nanogui import refresh
    from micropython_nano_gui.core.writer import Writer
    from micropython_nano_gui.widgets.label import Label

    # Fonts
    import micropython_nano_gui.fonts.arial10 as arial10
    import micropython_nano_gui.fonts.freesans20 as freesans20
    import micropython_nano_gui.fonts.arial35 as arial35

    HOSTED = False
except:
    HOSTED = True

from time import sleep


from departure_time_info import DepartureTimeInfo

ssd = None

# Pin Definitions
RST_PIN = 12
DC_PIN = 8
CS_PIN = 9
BUSY_PIN = 13

# Gui infrastructure definitions
wri = None


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
    ssd = SSD(spi, pcs, pdc, prst, pbusy, landscape=True, asyn=False, full=True)

    global wri
    wri = Writer(ssd, arial35, verbose=False)
    wri.set_clip(True, True, False)

    ssd.init_partial()


first_display = True


def display_update(departure_list: list[DepartureTimeInfo]):
    if HOSTED:
        return

    global first_display
    if first_display == True:
        ssd.set_full()
        first_display = False

    else:
        ssd.set_partial()

    row_pos = 2
    col_pos = 2
    for departure in departure_list[:3]:
        wri.set_textpos(ssd, col_pos, row_pos)
        wri.printstring(
            f"{departure.service:3}{departure.destination:8}{departure.time:>8}"
        )
        col_pos += 40

    ssd.show()
    ssd.wait_until_ready()


def display_clear(ssd):
    refresh(ssd, True)
