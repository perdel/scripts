#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import datetime
import sys
import numpy as np
import matplotlib.pyplot as plt


def measure(power_file: str, out_file: str) -> None:
    """Measure energy consumption"""
    t0 = time.time()

    while True:
        with open(power_file, mode="r") as f:
            line = f.readlines()
            line = float(line[0].strip()) / 1e6
            with open(out_file, mode="a") as o:
                delta_t = time.time() - t0
                o.write(f"{delta_t:.2f} {line:.3f}\n")
        time.sleep(10)


def analyse(fname: str, supply_price: float) -> None:
    """Analyse energy consumption"""
    data = np.loadtxt(fname)
    time_h = data[:, 0] / 3600
    time_str = str(datetime.timedelta(seconds=int(data[-1, 0])))
    energy = np.trapz(data[:, 1], time_h) / 1000
    price = energy * supply_price
    mean = float(np.mean(data[:, 1]))
    _, ax = plt.subplots()
    plt.xlabel(r"Time (h)")
    plt.ylabel(r"Power (W)")
    plt.xlim(0, time_h[-1])
    plt.ylim(0, int(np.max(data[:, 1])) + 1)
    plt.plot(time_h, data[:, 1])
    plt.axhline(mean, linestyle="dashed")
    summary = f"Energy: {energy:.3f} kWh\nTime: {time_str} h\nMean power: {mean:.3f} W\nPrice: {price:.2f} €"
    plt.text(0.75, 0.25, summary, transform=ax.transAxes)
    plt.show()


if __name__ == "__main__":
    POWER_FILE = "/sys/class/power_supply/BAT0/power_now"
    OUTFILE = f"stats_{datetime.date.today().isoformat()}"
    SUPPLY_PRICE = 0.3189

    if sys.argv[1] == "-m":
        measure(power_file=POWER_FILE, out_file=OUTFILE)
    elif sys.argv[1] == "-a":
        analyse(fname=sys.argv[2], supply_price=SUPPLY_PRICE)
    else:
        print("Unknown option")
        sys.exit()
