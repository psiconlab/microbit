from microbit import *
import music
import neopixel

t = 1
mode = 1
timeNow = 0
lastTime = 0

# Joystick
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
lPos = 0
nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
nPos = 9

# LEDs
npix = neopixel.NeoPixel(pin13, 6)
nocol = (0, 0, 0)
r = (54, 0, 0)
g = (0, 54, 0)
b = (0, 0, 54)
y = (54, 54, 0)
l = (1, 1, 2)
n = (2, 2, 1)

# Codes
pos = 0
combo = []

code1 = ["y", "r", "1", "B", "1", "B"]
clue1 = ["C", "O", "A", "C", "H"]

code2 = ["r", "g", "b", "b", "g", "r"]
clue2 = [1, 1, 2, 3]

code3 = ["b", "r", "y", "y", "r", "b"]
clue3 = [2, 5, 1]

code4 = ["r", "r", "r", "b", "b", "b"]
clue4 = ["YOU DID IT!"]

codes = [code1, code2, code3, code4]
clues = [clue1, clue2, clue3, clue4]


def test():
    print("User : "+str(combo))
    ok = 0
    puzzle = 0
    for item in codes[:]:
        if str(combo) == str(item):
            print("Match!")
            ok = 1
            if puzzle == len(codes)-1:
                music.play(music.BADDY)
            else:
                music.play(music.BA_DING)
                sleep(3000)
            for n in range(0, len(clues[puzzle])):
                display.scroll(str(clues[puzzle][n]))
                sleep(1000)
                display.clear()
                sleep(500)
            break
        puzzle += 1
        print("Puzzle : "+str(item))
    if ok == 0:
        print("No match...")
        music.play(music.WAWAWAWAA)
    tidy()


def light_led(col):
    global pos
    npix[pos] = col
    npix.show()


def all_leds(col):
    for pix in range(0, len(npix)):
        npix[pix] = col
    npix.show()


def tidy():
    global combo, lPos, nPos, pos
    display.clear()
    all_leds(nocol)
    combo = []
    lPos = 0
    nPos = 0
    pos = 0
    sleep(1500)


def buttons():
    global lPos, letters, nPos, nums, mode, combo

    if pin12.read_digital() == 1:
        # red button
        light_led(r)
        new_item("r")

    if pin15.read_digital() == 1:
        # blue button
        light_led(b)
        new_item("b")

    if pin14.read_digital() == 1:
        # green button
        light_led(g)
        new_item("g")

    if pin16.read_digital() == 1:
        # yellow button
        light_led(y)
        new_item("y")

    if pin8.read_digital():
        # a letter or number has been selected
        if mode == 1:
            light_led(l)
            new_item(letters[lPos])
        elif mode == 0:
            light_led(n)
            new_item(nums[nPos])


def joyTouched(m):
    global t, mode, lastTime
    t = 1
    mode = m
    lastTime = int(running_time())
    sleep(250)


def joystick():
    global lPos, letters, nPos, nums
    global mode, t, lastTime, timeNow

    # joystick - up down - numbers
    joy_ud = pin2.read_analog()
    if joy_ud < 150:
        nPos -= 1
        joyTouched(0)
    elif joy_ud > 750:
        nPos += 1
        joyTouched(0)

    # joystick - left right - letters
    joy_lr = pin1.read_analog()
    if joy_lr < 150:
        lPos -= 1
        joyTouched(1)
    elif joy_lr > 750:
        lPos += 1
        joyTouched(1)
        
    if lPos > 25:
        lPos = 0
    if lPos < 0:
        lPos = 25
    if nPos > 9:
        nPos = 0
    if nPos < 0:
        nPos = 9

    # show blinking display
    if t > 0:
        if mode == 1:
            display.show(letters[lPos])
        elif mode == 0:
            display.show(nums[nPos])
    else:
        display.clear()

    # blink timer
    timeNow = int(running_time())
    if timeNow > lastTime + 500:
        t *= -1
        lastTime = timeNow


def new_item(i):
    global pos
    combo.append(i)
    pos += 1
    if pos == 6:
        test()
    sleep(200)


while True:
    buttons()
    joystick()
    sleep(20)
