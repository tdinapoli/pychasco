import pycct
import matplotlib.pyplot as plt
import RPi.GPIO as gpio
from typing import Literal


def find_spec():
    print("looking for /dev/ttyACM devices...")
    for i in range(5):
        try:
            spec = pycct.spectrometer.Spectrometer(port=f"/dev/ttyACM{i}")
        except TimeoutError:
            print(f"/dev/ttyACM{i} not found")
            continue
        return spec
    print("no /dev/ttyACM devices found. Looking for /dev/USB devices...")
    for i in range(5):
        try:
            spec = pycct.spectrometer.Spectrometer(port=f"/dev/ttyUSB{i}")
        except TimeoutError:
            print(f"/dev/ttyUSB{i} not found")
            continue
        return spec
    print("no devices found.")
    exit()


def init_gpio():
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)

    gpio.setup(5, gpio.OUT, initial=gpio.LOW)
    gpio.setup(6, gpio.OUT, initial=gpio.LOW)


def measure(
    spec: pycct.spectrometer.Spectrometer,
    led: Literal["blue", "uv"],
    tint: float,
    avgs: int,
    amplitude_corrected: bool,
):
    if led == "blue":
        pin = 5
    elif led == "uv":
        pin = 6
    else:
        raise ValueError("wrong led pin number")

    gpio.output(pin, gpio.HIGH)
    tst, wls, cts = spec.acquire_single_spectrum()
    gpio.output(pin, gpio.LOW)
    return tst, wls, cts


def main():
    print("hello")

    TINT = 10
    AVGS = 1
    LED = "blue"
    CORRECTED = False
    init_gpio()
    spec = find_spec()
    print("connected")

    tst, wls, cts = measure(spec, LED, TINT, AVGS, CORRECTED)

    plt.plot(
        wls, cts, label=f"led {LED}, tint {TINT}, avgs {AVGS}, corrected {CORRECTED}"
    )
    plt.xlabel("wavelength (nm)")
    plt.ylabel("Intensity")
    plt.legend()
    plt.savefig("spectrum.png", dpi=300)


if __name__ == "__main__":
    main()
