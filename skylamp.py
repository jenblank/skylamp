from math import pi
import ephem
import serial

# setup serial port where arduino is
ser = serial.Serial('/dev/cu.usbmodem1421', 9600)

# setup pyephem Observer location and date/time
location = ephem.Observer()
location.lat = ephem.degrees("37.7749")
location.long = ephem.degrees("-122.4194")
location.date = "2016/12/11 03:40:300"  # must be GMT

mer = ephem.Mercury(location)
ven = ephem.Venus(location)
mar = ephem.Mars(location)
jup = ephem.Jupiter(location)
sat = ephem.Saturn(location)

# Azimuth usually starts from North
planets = {
    'mercury': (mer.alt, mer.az, mer.mag),
    'venus': (ven.alt, ven.az, ven.mag),
    'mars': (mar.alt, mar.az, mar.mag),
    'jupiter': (jup.alt, jup.az, jup.mag),
    'saturn': (sat.alt, sat.az, sat.mag),
}

# nastyh hacker
pin_code = {
    ('mercury','E'): 1,
    ('mercury','C'): 2,
    ('mercury','W'): 3,
    ('venus','E'): 4,
    ('venus','C'): 5,
    ('venus','W'): 6,
    ('mars','E'): 7,
    ('mars','C'): 8,
    ('mars','W'): 9,
    ('jupiter','E'): 10,
    ('jupiter','C'): 11,
    ('jupiter','W'): 12,
    ('saturn','E'): 13,
    ('saturn','C'): 14,
    ('saturn','W'): 15
}


# < 135 East light -- 135 to 225 Center Light -- > 225 West light
for p, i in planets.items():
    alt, az, mag = i

    if 180 * alt / pi < 5:
        continue # planet is below the horizon

    az_degrees = 180 * az / pi
    if az_degrees <= 135:
        # planet is in the East
        direction = "E"

    if az_degrees > 135 and az_degrees < 225:
        # planet is in the South
        direction = "S"

    if az_degrees >= 135:
        # planet is in the West
        direction = "W"

    msg = pin_code[p, direction]
    ser.write(str(msg))
