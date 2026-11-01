
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# muutujad
jalakaija_soov = False

autode_punane = 11
autode_kollane = 13
autode_roheline = 15

jalakaijate_punane = 16
jalakaijate_roheline = 18

nupu_indikaator = 29
nupp = 31

# setup
GPIO.setup(autode_punane, GPIO.OUT)
GPIO.setup(autode_kollane, GPIO.OUT)
GPIO.setup(autode_roheline, GPIO.OUT)

GPIO.setup(jalakaijate_punane, GPIO.OUT)
GPIO.setup(jalakaijate_roheline, GPIO.OUT)

GPIO.setup(nupu_indikaator, GPIO.OUT)
GPIO.setup(nupp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# kontrollib nuppu
def kontrolli_nuppu():
    global jalakaija_soov

    if GPIO.input(nupp) == GPIO.HIGH:
        jalakaija_soov = True
        GPIO.output(nupu_indikaator, GPIO.HIGH)

# ootab ja kontrollib samal ajal nuppu
def oota(aeg):
    for i in range(int(aeg * 100)):
        kontrolli_nuppu()
        time.sleep(0.01)


try:
    while True:

        # autode punane
        GPIO.output(autode_punane, GPIO.HIGH)

        if jalakaija_soov:
            GPIO.output(nupu_indikaator, GPIO.LOW)
            GPIO.output(jalakaijate_punane, GPIO.LOW)
            GPIO.output(jalakaijate_roheline, GPIO.HIGH)

            jalakaija_soov = False
        else:
            GPIO.output(jalakaijate_punane, GPIO.HIGH)
            GPIO.output(jalakaijate_roheline, GPIO.LOW)

        oota(5)

        GPIO.output(autode_punane, GPIO.LOW)
        GPIO.output(jalakaijate_roheline, GPIO.LOW)
        GPIO.output(jalakaijate_punane, GPIO.HIGH)

        # autode kollane
        GPIO.output(autode_kollane, GPIO.HIGH)
        oota(1)
        GPIO.output(autode_kollane, GPIO.LOW)

        # autode roheline
        GPIO.output(autode_roheline, GPIO.HIGH)
        oota(5)
        GPIO.output(autode_roheline, GPIO.LOW)

        # autode kollane vilgub
        for i in range(3):
            GPIO.output(autode_kollane, GPIO.HIGH)
            oota(1 / 3)

            GPIO.output(autode_kollane, GPIO.LOW)
            oota(1 / 3)

except KeyboardInterrupt:
    print("Programm peatatud")

finally:
    GPIO.cleanup()
