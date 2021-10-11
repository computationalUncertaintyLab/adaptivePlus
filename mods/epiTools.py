#mcandrew
def fromEW2Season(ew):
    yr = int(str(ew)[:4])
    wk = int(str(ew)[4:])
    return "{:d}/{:d}".format(yr,yr+1) if 40<=wk<=53 else "{:d}/{:d}".format(yr-1,yr)
