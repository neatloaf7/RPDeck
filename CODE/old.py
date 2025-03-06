import board
import rotaryio
import digitalio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import usb_hid
import time
import displayio
import busio
import adafruit_displayio_sh1106
from adafruit_display_text import label
import terminalio
import usb_cdc
import adafruit_imageload

serial = usb_cdc.data

# Release any existing displays
displayio.release_displays()

# Initialize I2C
i2c = busio.I2C(scl=board.GP3, sda=board.GP2, frequency=400000)

# Create the display bus
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)  # Use 0x3D if address is different

# Create the SH1106 display object
display = adafruit_displayio_sh1106.SH1106(display_bus, width=132, height=64)

# Create a display group
splash = displayio.Group()

bitmap , palette1 = adafruit_imageload.load("width.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
print("BMP file loaded successfully!")
print("Bitmap width:", bitmap.width)
print("Bitmap height:", bitmap.height)


bitmap2, palette = adafruit_imageload.load("/eyb.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
palette.make_transparent(0x000000)
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette1)
grid2 = displayio.TileGrid(bitmap2, pixel_shader=palette)

bitmap3 = displayio.OnDiskBitmap("tall.bmp")
tallgrid = displayio.TileGrid(bitmap3, pixel_shader=palette,tile_width=128,tile_height=64,width=1,height=2)

splash.append(tile_grid)

# Show the group on the display
display.root_group = splash



"""
WIDTH = 128
HEIGHT = 32
BORDER = 5
color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER)
splash.append(inner_sprite)

# Draw a label
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=HEIGHT // 2 - 1)
splash.append(text_area)
"""
##################################################################################

# Initialize Encoder 1
encoder1 = rotaryio.IncrementalEncoder(board.GP7, board.GP8)
encoder2 = rotaryio.IncrementalEncoder(board.GP14, board.GP15)
last_position1 = encoder1.position
last_position2 = encoder2.position

# Initialize Button 1
button1 = digitalio.DigitalInOut(board.GP6)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP

button2 = digitalio.DigitalInOut(board.GP13)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP

# initialize keyboard
kbd = Keyboard(usb_hid.devices)


while True:
    # Read Encoder 1
    position1 = encoder1.position
    position2 = encoder2.position
    position1_change = position1 - last_position1
    position2_change = position2 - last_position2

    if position1 != last_position1:
        print("Encoder 1 Position:", position1)
        if position1_change > 0:
            message = "a ~"
            serial.write(message.encode('utf-8'))
            tallgrid[0]=0
            splash.append(tallgrid)
            last_position1 = position1
        if position1_change < 0:
            tallgrid[0]=1
            last_position1 = position1


    if position2 != last_position2:
        print("Encoder 2 Position:", position2)
        last_position2 = position2

    # Read Button 1
    if not button1.value:
        print("Button 1 Pressed")

    if not button2.value:
        print("Button 2 Pressed")
        pass
