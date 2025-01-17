#!/usr/bin/python3
# coding: utf-8
import time
import gi

gi.require_version("Notify", "0.7")
from gi.repository import Notify


def get_file_info(name):
    root_dir = "/sys/class/power_supply/BAT0"
    fp = open(f"{root_dir}/{name}", mode="r")
    output = fp.readline()
    fp.close()
    return output.strip()


def call_notify(level, msg):
    level = level.lower()
    message = Notify.Notification.new("Battery", msg)
    if level == "low":
        message.set_urgency(Notify.Urgency.LOW)
    elif level == "normal":
        message.set_urgency(Notify.Urgency.NORMAL)
    elif level == "critical":
        message.set_urgency(Notify.Urgency.CRITICAL)
    else:
        raise (IOError)
    message.show()


LOWER_LIMIT = 4
UPPER_LIMIT = 95
SLEEP_TIME = 120
Notify.init("Battery")

while True:
    status = get_file_info("status")
    capacity = int(get_file_info("capacity"))
    if status == "Charging":
        if capacity > UPPER_LIMIT:
            txt = "Fully charged."
            call_notify("LOW", txt)
        sleep_time = 5 * SLEEP_TIME
    else:
        if capacity > LOWER_LIMIT * 3:
            sleep_time = 2 * SLEEP_TIME
        elif LOWER_LIMIT < capacity < LOWER_LIMIT * 3:
            sleep_time = SLEEP_TIME
        elif capacity < LOWER_LIMIT:
            txt = "Capacity is low!"
            call_notify("CRITICAL", txt)
            sleep_time = SLEEP_TIME
    time.sleep(sleep_time)
