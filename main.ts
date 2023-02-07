function resetinnstillinger () {
    motor_på = false
    gasspedalinput = 0
    rattinput = 0
    offtrack_faktor = 1
    RCstoppet = false
    racestart_pågår = false
    tjuvstart = false
}
function éntilnullindeksering (énindeksert_tall: number) {
    if (énindeksert_tall % 10 != 0) {
        return énindeksert_tall - 1
    } else {
        return 10 - 1
    }
}
// Slik LED-lysene lyser når bilmotore er skrudd av.
// De bakerste lysene i hovedfargen, de to fremste i støttefargene
function LEDlys_parkert () {
    bitbot.ledBrightness(40)
    for (let kolonne = 0; kolonne <= 1; kolonne++) {
        for (let rad = 0; rad <= 1; rad++) {
            bitbot.setPixelColor(6 * kolonne + (0 + rad), lagfarge_hoved)
            bitbot.setPixelColor(6 * kolonne + (2 + rad), lagfarge_sving)
            bitbot.setPixelColor(6 * kolonne + (4 + rad), lagfarge_hoved)
        }
    }
}
function oppdater_lagLED () {
    if (lagnr == 1) {
        sett_lagfarge(0x0000FF, 0xFF0000)
    } else if (lagnr == 2) {
        sett_lagfarge(0xFF0000, 0xFFFF00)
    } else if (lagnr == 3) {
        sett_lagfarge(bitbot.convertRGB(0, 100, 20), bitbot.convertRGB(40, 40, 40))
    } else if (lagnr == 4) {
        sett_lagfarge(0xFF00FF, 0x0080FF)
    } else if (lagnr == 5) {
        sett_lagfarge(bitbot.convertRGB(180, 80, 0), 0x00FFFF)
    } else if (lagnr == 6) {
        sett_lagfarge(bitbot.convertRGB(100, 0, 0), 0xFFFFFF)
    } else if (lagnr == 7) {
        sett_lagfarge(bitbot.convertRGB(6, 54, 8), bitbot.convertRGB(200, 255, 0))
    } else if (lagnr == 8) {
        sett_lagfarge(bitbot.convertRGB(50, 50, 50), 0xFF0000)
    } else if (lagnr == 9) {
        sett_lagfarge(bitbot.convertRGB(0, 0, 60), 0xFFFFFF)
    } else if (lagnr == 0) {
        sett_lagfarge(0x0080FF, 0x0000FF)
    }
}
function bytt_lag (opp_eller_ned: number) {
    lagnr += opp_eller_ned
    if (lagnr >= 10) {
        lagnr = 0
    } else if (lagnr < 0) {
        lagnr = 9
    }
    oppdater_lagLED()
    radio.sendValue("lagnr", lagnr)
    vis_skjerm_alternerende_RCstopp()
}
function vis_radionr_uten_scroll () {
    if (radionr < 10) {
        basic.showNumber(radionr, 0)
    } else {
        tall_tosifra[radionr - 10].showImage(0, 0)
    }
}
function motor_PÅ () {
    motor_på = true
}
function lights_out (forsinkelse: number) {
    vis_radionr_uten_scroll()
    tid_siste_kjøresignal_mottatt = control.millis()
    bitbot.ledClear()
    racestart_pågår = true
    for (let rad = 0; rad <= 4; rad++) {
        basic.pause(1000)
        bitbot.setPixelColor(rad, lagfarge_hoved)
        bitbot.setPixelColor(6 + rad, lagfarge_hoved)
    }
    basic.pause(1000 + forsinkelse)
    bitbot.ledClear()
    basic.pause(200)
    motor_på = true
    RCstoppet = false
    racestart_pågår = false
    gasspedalinput = 5
}
function tenn_LED (kol: number, rad: number, fram: boolean) {
    if (fram) {
        return 6 * kol + (5 - rad)
    } else {
        return 6 * kol + rad
    }
}
function vis_skjerm_alternerende_RCstopp () {
    if ((control.millis() - tid_siste_RCsynk) / 1000 % 6 < 3) {
        basic.showIcon(IconNames.StickFigure)
    } else {
        vis_radionr_uten_scroll()
    }
}
radio.onReceivedString(function (receivedString) {
    if (receivedString == "ratt_start") {
        motor_PÅ()
    } else if (receivedString == "ratt_stopp") {
        motor_AV()
    }
    if (receivedString == "RC_stopp") {
        tid_siste_RCsynk = control.millis()
        RCstoppet = true
        motor_på = false
        gasspedalinput = 0
    } else if (receivedString == "RC_start") {
        tid_siste_RCsynk = control.millis()
        RCstoppet = false
        vis_radionr_uten_scroll()
    }
    if (receivedString == "ratt_restart") {
        resetinnstillinger()
        basic.showIcon(IconNames.Square)
        oppdater_lagLED()
        vis_radionr_uten_scroll()
    }
    if (receivedString == "tjuvstarta") {
        tjuvstartspinn()
    }
})
function opprett_ikoner () {
    // ett bilde: 60 kB
    tall_tosifra = [
    images.createImage(`
        # . # # #
        # . # . #
        # . # . #
        # . # . #
        # . # # #
        `),
    images.createImage(`
        . # . . #
        # # . # #
        . # . . #
        . # . . #
        . # . . #
        `),
    images.createImage(`
        # . # # #
        # . . . #
        # . # # #
        # . # . .
        # . # # #
        `),
    images.createImage(`
        # . # # #
        # . . . #
        # . # # #
        # . . . #
        # . # # #
        `),
    images.createImage(`
        # . # . #
        # . # . #
        # . # # #
        # . . . #
        # . . . #
        `),
    images.createImage(`
        # . # # #
        # . # . .
        # . # # #
        # . . . #
        # . # # #
        `),
    images.createImage(`
        # . # # #
        # . # . .
        # . # # #
        # . # . #
        # . # # #
        `),
    images.createImage(`
        # . # # #
        # . . . #
        # . . . #
        # . . . #
        # . . . #
        `),
    images.createImage(`
        # . # # #
        # . # . #
        # . # # #
        # . # . #
        # . # # #
        `),
    images.createImage(`
        # . # # #
        # . # . #
        # . # # #
        # . . . #
        # . # # #
        `),
    images.createImage(`
        # # . . .
        . # . . .
        # # . # #
        # . . # #
        # # . # #
        `)
    ]
}
function tjuvstartspinn () {
    tjuvstart = true
    basic.showIcon(IconNames.Confused)
    bitbot.ledClear()
    for (let indeks = 0; indeks <= 12; indeks++) {
        if (indeks < 6) {
            bitbot.setPixelColor(indeks, lagfarge_hoved)
        } else {
            bitbot.setPixelColor(17 - indeks, lagfarge_hoved)
        }
        bitbot.rotatems(BBRobotDirection.Left, 100, 80)
    }
    tjuvstart = false
}
function hastighet_omregnet () {
    if (bitbot.readLine(BBLineSensor.Left) == 0 && bitbot.readLine(BBLineSensor.Right) == 0) {
        if (control.millis() - tid_siste_offtrack < 3000) {
            offtrack_faktor += 0.004
        } else {
            offtrack_faktor = 1
        }
    } else if (bitbot.readLine(BBLineSensor.Left) == 1 && bitbot.readLine(BBLineSensor.Right) == 1) {
        offtrack_faktor = 0.2
        tid_siste_offtrack = control.millis()
    } else {
        offtrack_faktor = 0.4
        tid_siste_offtrack = control.millis()
    }
    if (gasspedalinput < 0) {
        offtrack_faktor = Math.sqrt(offtrack_faktor)
    }
    return Math.abs(gasspedalinput * offtrack_faktor)
}
radio.onReceivedValue(function (name, value) {
    tid_siste_kjøresignal_mottatt = control.millis()
    if (name == "RC_5L") {
        tid_siste_RCsynk = control.millis()
        lights_out(value)
    }
    if (name == "fart") {
        gasspedalinput = value
    }
    if (name == "sving") {
        rattinput = value
    }
})
function motor_AV () {
    LEDlys_parkert()
    motor_på = false
    gasspedalinput = 0
}
function LEDlys_kjører_v3 () {
    bitbot.ledBrightness(90)
    fartslysNr_tennes = Math.round(pins.map(
    Math.abs(hastighet_omregnet()),
    0,
    100,
    0,
    5
    ))
    if (gasspedalinput == 0) {
        for (let kolonne = 0; kolonne <= 1; kolonne++) {
            for (let rad = 0; rad <= 1; rad++) {
                bitbot.setPixelColor(6 * kolonne + rad, 0x000000)
                bitbot.setPixelColor(6 * kolonne + (2 + rad), lagfarge_hoved)
                bitbot.setPixelColor(6 * kolonne + (4 + rad), 0x000000)
            }
        }
    } else {
        svinglysNr_tennes = Math.round(pins.map(
        Math.abs(rattinput),
        0,
        80,
        -1,
        fartslysNr_tennes
        ))
        for (let rad = 0; rad <= 5; rad++) {
            for (let kolonne = 0; kolonne <= 1; kolonne++) {
                if (rad <= fartslysNr_tennes) {
                    if (rad <= svinglysNr_tennes) {
                        // venstresving
                        // kolonne = 0 betyr venstre kolonne av LED-lys (0–5)
                        // høyresving
                        // kolonne = 1 betyr høyre kolonne av LED-lys (6–11)
                        if (rattinput < 0 && kolonne == 0) {
                            bitbot.setPixelColor(tenn_LED(kolonne, rad, gasspedalinput > 0), lagfarge_sving)
                        } else if (rattinput > 0 && kolonne == 1) {
                            bitbot.setPixelColor(tenn_LED(kolonne, rad, gasspedalinput > 0), lagfarge_sving)
                        } else {
                            bitbot.setPixelColor(tenn_LED(kolonne, rad, gasspedalinput > 0), lagfarge_hoved)
                        }
                    } else {
                        bitbot.setPixelColor(tenn_LED(kolonne, rad, gasspedalinput > 0), lagfarge_hoved)
                    }
                } else {
                    bitbot.setPixelColor(tenn_LED(kolonne, rad, gasspedalinput > 0), 0x000000)
                }
            }
        }
    }
}
function svingjustert_fart () {
    return hastighet_omregnet() - Math.abs(0.7 * rattinput)
}
function sett_lagfarge (farge1: number, farge2: number) {
    lagfarge_hoved = farge1
    lagfarge_sving = farge2
}
function stopp_hvis_inaktiv_bil_etter (sek: number) {
    if (control.millis() - tid_siste_kjøresignal_mottatt > sek * 1000) {
        motor_AV()
    }
}
let svinglysNr_tennes = 0
let fartslysNr_tennes = 0
let tid_siste_offtrack = 0
let tid_siste_RCsynk = 0
let tid_siste_kjøresignal_mottatt = 0
let tall_tosifra: Image[] = []
let lagfarge_sving = 0
let lagfarge_hoved = 0
let tjuvstart = false
let racestart_pågår = false
let RCstoppet = false
let offtrack_faktor = 0
let rattinput = 0
let gasspedalinput = 0
let motor_på = false
let lagnr = 0
let radionr = 0
radionr = 5
radio.setGroup(radionr)
radio.sendString("bil_restart")
resetinnstillinger()
lagnr = radionr % 10
oppdater_lagLED()
LEDlys_parkert()
opprett_ikoner()
vis_radionr_uten_scroll()
basic.pause(1000)
basic.forever(function () {
    if (!(racestart_pågår || tjuvstart)) {
        if (motor_på && !(RCstoppet)) {
            if (gasspedalinput >= 0) {
                bitbot.go(BBDirection.Forward, hastighet_omregnet())
            } else {
                bitbot.go(BBDirection.Reverse, hastighet_omregnet())
            }
            if (rattinput >= 0) {
                bitbot.BBBias(BBRobotDirection.Right, rattinput)
            } else {
                bitbot.BBBias(BBRobotDirection.Left, Math.abs(rattinput))
            }
            LEDlys_kjører_v3()
        } else {
            bitbot.stop(BBStopMode.Brake)
            LEDlys_parkert()
        }
        stopp_hvis_inaktiv_bil_etter(30)
    }
    if (RCstoppet && !(racestart_pågår)) {
        vis_skjerm_alternerende_RCstopp()
    }
})
