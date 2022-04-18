from RfcParser import RFC

with open("data/rfc3261.txt") as f:
    rfc3261 = RFC(f.read())


with open("data/rfc2119.txt") as f:
    rfc2119 = RFC(f.read())


with open("data/rfc2327.txt") as f:
    rfc2327 = RFC(f.read())
