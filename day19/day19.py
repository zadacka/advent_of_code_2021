

# scanner #1 is the 'origin' - we will use it as a reference

# for scanner in scanners[1:]

# this scanner can report its set of beacons with 24 different coordinates
# depending on how it is rotated.
# Generate a set of all of them so that we have ONE that matches the orientation of scanner 'origin'

# for each rotation....
# for each beacon in the 'origin' set, generate the relative position to each scanner in the 'candidate' set
# if we have 12 (or more) maps that are the same ... then we're a go! That rotation is a correct match

# for each beacon in the new known set (of the correct orientation) ... shift it by the mapping
# ... then continue with the next scanner