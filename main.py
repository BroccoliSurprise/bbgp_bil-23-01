def on_received_number(receivedNumber):
    global tid_siste_kjøresignal_mottatt, kjøreretning_fram, gasspedalinput, svingretning_venstre, rattinput
    tid_siste_kjøresignal_mottatt = control.millis()
    if receivedNumber > 0:
        if receivedNumber >= 1000:
            kjøreretning_fram = True
            gasspedalinput = receivedNumber - 1000
        else:
            kjøreretning_fram = False
            gasspedalinput = receivedNumber - 100
    elif receivedNumber <= -1000:
        svingretning_venstre = True
        rattinput = abs(receivedNumber + 1000)
    else:
        svingretning_venstre = False
        rattinput = abs(receivedNumber + 100)
radio.on_received_number(on_received_number)

def vis_skjerm_momentant(tall: number):
    global teksttabell
    teksttabell = [images.create_image("""
            . . # . .
                    . . # . .
                    . . # . .
                    . . # . .
                    . . # . .
        """),
        images.create_image("""
            . # # # .
                    . . . # .
                    . # # # .
                    . # . . .
                    . # # # .
        """),
        images.create_image("""
            . # # # .
                    . . . # .
                    . # # # .
                    . . . # .
                    . # # # .
        """),
        images.create_image("""
            . # . # .
                    . # . # .
                    . # # # .
                    . . . # .
                    . . . # .
        """),
        images.create_image("""
            . # # # .
                    . # . . .
                    . # # # .
                    . . . # .
                    . # # # .
        """),
        images.create_image("""
            . # # # .
                    . # . . .
                    . # # # .
                    . # . # .
                    . # # # .
        """)]
    teksttabell[tall].show_image(0, 0)
def resetinnstillinger():
    global motor_på, gasspedalinput, rattinput, kjøreretning_fram, svingretning_venstre, offtrack_faktor, RCstoppet, racestart_pågår, tjuvstart
    motor_på = False
    gasspedalinput = 0
    rattinput = 0
    kjøreretning_fram = True
    svingretning_venstre = True
    offtrack_faktor = 1
    RCstoppet = False
    racestart_pågår = False
    tjuvstart = False
# Slik LED-lysene lyser når bilmotore er skrudd av.
# De bakerste lysene i hovedfargen, de to fremste i støttefargene
def LEDlys_parkert():
    bitbot.led_brightness(40)
    for kolonne in range(2):
        for rad in range(2):
            bitbot.set_pixel_color(6 * kolonne + (0 + rad), lagfarge_hoved)
            bitbot.set_pixel_color(6 * kolonne + (2 + rad), lagfarge_sving)
            bitbot.set_pixel_color(6 * kolonne + (4 + rad), lagfarge_hoved)
def oppdater_lagLED():
    if lagnr == 1:
        sett_lagfarge(bitbot.convert_rgb(0, 100, 20),
            bitbot.convert_rgb(40, 40, 40))
    elif lagnr == 2:
        sett_lagfarge(255, 16711680)
    elif lagnr == 3:
        sett_lagfarge(16711680, 16776960)
    elif lagnr == 4:
        sett_lagfarge(bitbot.convert_rgb(180, 80, 0), 65535)
    elif lagnr == 5:
        sett_lagfarge(16711935, 33023)
    elif lagnr == 6:
        sett_lagfarge(bitbot.convert_rgb(0, 0, 60), 16777215)
    elif lagnr == 7:
        sett_lagfarge(bitbot.convert_rgb(6, 54, 8),
            bitbot.convert_rgb(200, 255, 0))
    elif lagnr == 8:
        sett_lagfarge(33023, 255)
    elif lagnr == 9:
        sett_lagfarge(bitbot.convert_rgb(100, 0, 0), 16777215)
    elif lagnr == 0:
        sett_lagfarge(bitbot.convert_rgb(50, 50, 50), 16711680)
def tenn_LED_foran_til_bak(k: number, r: number):
    return 6 * k + (5 - r)
def bytt_lag(opp_eller_ned: number):
    global lagnr
    lagnr += opp_eller_ned
    if lagnr >= 10:
        lagnr = 0
    elif lagnr < 0:
        lagnr = 9
    oppdater_lagLED()
    radio.send_value("lagnr", lagnr)
    skjerm_nr_og_logo()
def motor_PÅ():
    global motor_på
    motor_på = True
def lights_out(forsinkelse: number):
    global tid_siste_kjøresignal_mottatt, racestart_pågår, motor_på, RCstoppet, gasspedalinput
    tid_siste_kjøresignal_mottatt = control.millis()
    bitbot.led_clear()
    racestart_pågår = True
    for indeks2 in range(5):
        basic.pause(1000)
        bitbot.set_pixel_color(indeks2, lagfarge_hoved)
        bitbot.set_pixel_color(6 + indeks2, lagfarge_hoved)
    basic.pause(forsinkelse)
    bitbot.led_clear()
    basic.pause(200)
    motor_på = True
    RCstoppet = False
    racestart_pågår = False
    gasspedalinput = 5
def lagre_skjerm():
    global tabell
    tabell = []
    for kolonne2 in range(5):
        for rad2 in range(5):
            if led.point(kolonne2, rad2):
                tabell.append([kolonne2, kolonne2])
    return tabell
def tenn_LED_bak_til_foran(l: number, s: number):
    return 6 * l + s

def on_received_string(receivedString):
    global RCstoppet, motor_på, gasspedalinput
    if receivedString == "ratt_start":
        motor_PÅ()
    elif receivedString == "ratt_stopp":
        motor_AV()
    if receivedString == "RC_stopp":
        RCstoppet = True
        motor_på = False
        gasspedalinput = 0
    elif receivedString == "RC_start":
        RCstoppet = False
        basic.show_icon(IconNames.HAPPY)
        skjerm_nr_og_logo()
    if receivedString == "ratt_restart":
        resetinnstillinger()
        radio.send_value("lagnr", lagnr)
        basic.show_icon(IconNames.SQUARE)
        oppdater_lagLED()
        skjerm_nr_og_logo()
    if receivedString == "tjuvstarta":
        tjuvstartspinn()
radio.on_received_string(on_received_string)

def tjuvstartspinn():
    global tjuvstart
    tjuvstart = True
    basic.show_icon(IconNames.CONFUSED)
    bitbot.led_clear()
    for indeks in range(13):
        if indeks < 6:
            bitbot.set_pixel_color(indeks, lagfarge_hoved)
        else:
            bitbot.set_pixel_color(17 - indeks, lagfarge_hoved)
        bitbot.rotatems(BBRobotDirection.LEFT, 100, 80)
    skjerm_nr_og_logo()
    tjuvstart = False
def hastighet_omregnet():
    global offtrack_faktor
    if bitbot.read_line(BBLineSensor.LEFT) == 0 and bitbot.read_line(BBLineSensor.RIGHT) == 0:
        offtrack_faktor = 1
    elif bitbot.read_line(BBLineSensor.LEFT) == 1 and bitbot.read_line(BBLineSensor.RIGHT) == 1:
        offtrack_faktor = 0.2
    else:
        offtrack_faktor = 0.5
    if kjøreretning_fram == False:
        offtrack_faktor = Math.sqrt(offtrack_faktor)
    return gasspedalinput * offtrack_faktor

def on_received_value(name, value):
    global tid_siste_kjøresignal_mottatt
    tid_siste_kjøresignal_mottatt = control.millis()
    if name == "RC_5L":
        if RCstoppet:
            lights_out(value)
radio.on_received_value(on_received_value)

def motor_AV():
    global motor_på, gasspedalinput
    LEDlys_parkert()
    motor_på = False
    gasspedalinput = 0
def LEDlys_kjører_v3():
    global fartslysNr_tennes, svinglysNr_tennes
    bitbot.led_brightness(90)
    fartslysNr_tennes = Math.round(pins.map(hastighet_omregnet(), 0, 100, 0, 5))
    if gasspedalinput == 0:
        for kolonne3 in range(2):
            for rad3 in range(2):
                bitbot.set_pixel_color(6 * kolonne3 + rad3, 0x000000)
                bitbot.set_pixel_color(6 * kolonne3 + (2 + rad3), lagfarge_hoved)
                bitbot.set_pixel_color(6 * kolonne3 + (4 + rad3), 0x000000)
    else:
        svinglysNr_tennes = Math.round(pins.map(rattinput, 0, 100, -1, fartslysNr_tennes))
        if kjøreretning_fram:
            for rad4 in range(6):
                for kolonne4 in range(2):
                    if rad4 <= fartslysNr_tennes:
                        if rad4 <= svinglysNr_tennes:
                            if svingretning_venstre and kolonne4 == 0:
                                bitbot.set_pixel_color(tenn_LED_foran_til_bak(kolonne4, rad4), lagfarge_sving)
                            elif not (svingretning_venstre) and kolonne4 == 1:
                                bitbot.set_pixel_color(tenn_LED_foran_til_bak(kolonne4, rad4), lagfarge_sving)
                            else:
                                bitbot.set_pixel_color(tenn_LED_foran_til_bak(kolonne4, rad4), lagfarge_hoved)
                        else:
                            bitbot.set_pixel_color(tenn_LED_foran_til_bak(kolonne4, rad4), lagfarge_hoved)
                    else:
                        bitbot.set_pixel_color(tenn_LED_foran_til_bak(kolonne4, rad4), 0x000000)
        else:
            for rad5 in range(6):
                for kolonne5 in range(2):
                    if rad5 <= fartslysNr_tennes:
                        if rad5 <= svinglysNr_tennes:
                            if svingretning_venstre and kolonne5 == 0:
                                bitbot.set_pixel_color(tenn_LED_bak_til_foran(kolonne5, rad5), lagfarge_sving)
                            elif not (svingretning_venstre) and kolonne5 == 1:
                                bitbot.set_pixel_color(tenn_LED_bak_til_foran(kolonne5, rad5), lagfarge_sving)
                            else:
                                bitbot.set_pixel_color(tenn_LED_bak_til_foran(kolonne5, rad5), lagfarge_hoved)
                        else:
                            bitbot.set_pixel_color(tenn_LED_bak_til_foran(kolonne5, rad5), lagfarge_hoved)
                    else:
                        bitbot.set_pixel_color(tenn_LED_bak_til_foran(kolonne5, rad5), 0x000000)
def sett_lagfarge(farge1: number, farge2: number):
    global lagfarge_hoved, lagfarge_sving
    lagfarge_hoved = farge1
    lagfarge_sving = farge2
def skjerm_nr_og_logo():
    pass
def stopp_hvis_inaktiv_bil_etter(sek: number):
    global motor_på
    if control.millis() - tid_siste_kjøresignal_mottatt > sek * 1000:
        motor_AV()
        motor_på = False
svinglysNr_tennes = 0
fartslysNr_tennes = 0
tabell: List[List[number]] = []
lagfarge_sving = 0
lagfarge_hoved = 0
tjuvstart = False
racestart_pågår = False
RCstoppet = False
offtrack_faktor = 0
motor_på = False
teksttabell: List[Image] = []
rattinput = 0
svingretning_venstre = False
gasspedalinput = 0
kjøreretning_fram = False
tid_siste_kjøresignal_mottatt = 0
lagnr = 0
radionr = 3
radio.set_group(radionr)
radio.send_string("bil_restart")
resetinnstillinger()
lagnr = radionr % 10
oppdater_lagLED()
LEDlys_parkert()
basic.show_number(radionr)
skjerm_nr_og_logo()

def on_forever():
    if not (racestart_pågår or tjuvstart):
        if motor_på and not (RCstoppet):
            if kjøreretning_fram:
                bitbot.go(BBDirection.FORWARD, hastighet_omregnet())
            else:
                bitbot.go(BBDirection.REVERSE, hastighet_omregnet())
            if svingretning_venstre:
                bitbot.bb_bias(BBRobotDirection.LEFT, rattinput)
            else:
                bitbot.bb_bias(BBRobotDirection.RIGHT, rattinput)
            LEDlys_kjører_v3()
        else:
            bitbot.stop(BBStopMode.BRAKE)
            LEDlys_parkert()
        stopp_hvis_inaktiv_bil_etter(30)
    basic.clear_screen()
    if int(control.millis() / 1000) % 4 < 2:
        basic.show_number(radionr,0)
    else:
        vis_skjerm_momentant(radionr)
basic.forever(on_forever)
