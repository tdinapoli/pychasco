import pycct
import numpy as np


def main():
    print("hello")

    TINT = 10
    AVGS = 1
    spec = pycct.spectrometer.Spectrometer(port="/dev/ttyACM0")

    _, counts = spec.acquire_single_spectrum(TINT, AVGS)

    counts = np.array(counts)
    wls = spec.compute_wavelenghts()

    print(f"{counts=}")
    print(f"{wls=}")


if __name__ == "__main__":
    main()
