import board
import displayio
import busio
import adafruit_displayio_sh1106
import usb_cdc
import adafruit_imageload
import rotaryio
import time

#Release any existing displays
displayio.release_displays()

#Initialize I2C
i2c = busio.I2C(scl=board.D1, sda=board.D0)

#Make display bus
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)  # Use 0x3D if address is different

#Make SH1106 display object
display = adafruit_displayio_sh1106.SH1106(display_bus, width=132, height=64, brightness=0.1)
display.auto_refresh = False

#Import images
leftBmp, palette = adafruit_imageload.load("leftSprite.bmp", 
                                            bitmap = displayio.Bitmap,
                                            palette = displayio.Palette)
pusheenBmp, palette       = adafruit_imageload.load("pusheenSprite.bmp", 
                                            bitmap = displayio.Bitmap,
                                            palette = displayio.Palette)
speakerBmp, palette      = adafruit_imageload.load("speakerSprite.bmp", 
                                            bitmap = displayio.Bitmap,
                                            palette = displayio.Palette)
numBmp, palette          = adafruit_imageload.load("numSprite.bmp", 
                                            bitmap = displayio.Bitmap,
                                            palette = displayio.Palette)
#Create groups
group = displayio.Group()
leftGroup = displayio.Group()
pusheenGroup = displayio.Group(x=66, y=0)
speakerGroup = displayio.Group(x=66, y=32)
hundredGroup = displayio.Group(x=99, y=32)
tenGroup     = displayio.Group(x=107, y=32)
oneGroup     = displayio.Group(x=119, y=32)

#Create tilegrids
leftGrid = displayio.TileGrid(leftBmp, pixel_shader=palette,
                                width=1, height=1,
                                tile_width = 66, tile_height = 64)
pusheenGrid = displayio.TileGrid(pusheenBmp, pixel_shader=palette,
                                width=1, height=1,
                                tile_width = 66, tile_height = 32)
speakerGrid = displayio.TileGrid(speakerBmp, pixel_shader=palette,
                                width=1, height=1,
                                tile_width = 32 , tile_height = 32)
hundredGrid = displayio.TileGrid(numBmp, pixel_shader=palette,
                                width=1, height=1,
                                tile_width = 12, tile_height = 32)
tenGrid = displayio.TileGrid(numBmp, pixel_shader=palette,
                                width=1, height=1,
                                tile_width = 12, tile_height = 32)
oneGrid = displayio.TileGrid(numBmp, pixel_shader=palette,
                                width=1, height=1,
                                tile_width = 12, tile_height = 32)

leftGroup.append(leftGrid)
pusheenGroup.append(pusheenGrid)
speakerGrid[0] = 4
speakerGroup.append(speakerGrid)
hundredGrid[0]=11
hundredGroup.append(hundredGrid)
tenGroup.append(tenGrid)
oneGroup.append(oneGrid)


group.append(leftGroup)
group.append(pusheenGroup)
group.append(speakerGroup)
group.append(hundredGroup)
group.append(tenGroup)
group.append(oneGroup)

display.root_group = group
display.refresh()

#test stuff
volume = 00
profile = 0
encoder1 = rotaryio.IncrementalEncoder(board.D4, board.D3)
encoder2 = rotaryio.IncrementalEncoder(board.D7, board.D6)

lastPosition1 = encoder1.position
lastPosition2 = encoder2.position
lastVolume = volume
is100 = False
lastPush = time.monotonic()
frame = 0
framerate = .5

while True:
    now = time.monotonic()
    position1 = encoder1.position
    position2 = encoder2.position
    
    if position1 != lastPosition1:
        print("Encoder 1 position:", position1)
        if position1 > lastPosition1:
            if profile < 4:
                profile += 1     
            else:
                profile = 0      
        else:
            if profile > 0:
                profile -= 1
            else:
                profile = 4
        leftGrid[0] = profile
        display.refresh()
        lastPosition1 = position1

    if position2 != lastPosition2:
        print("Encoder 2 position", position2)
        if position2 > lastPosition2 and volume < 100:
            volume += 2
        if position2 < lastPosition2 and volume > 0:
            volume -= 2
        lastPosition2 = position2

    if volume != lastVolume:
        tenGrid[0] = (volume//10)%10
        oneGrid[0] = volume%10
        if volume < 100:
            if is100:
                is100 = False
                hundredGrid[0] = 11
        else:
            hundredGrid[0] = 10
            is100 = True
        display.refresh()
        lastVolume = volume

    if now - lastPush >= framerate:
        if frame < 3:
            frame += 1
        else:
            frame = 0
        pusheenGrid[0] = frame
        lastPush = now
        display.refresh()
            
    pass
