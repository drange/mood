stop = set()
with open("../stop.txt") as f:
    for line in f:
        line = line.strip().lower()
        ws = line.split()
        for w in ws:
            if w:
                stop.add(w)
stop = list(stop)
stop.sort()
for x in stop:
    print x
